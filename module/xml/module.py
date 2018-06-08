#
# Collective Knowledge (processing XML)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# validate XML against DTD

def validate(i):
    """
    Input:  {
              (data_uoa) - if specified use DTD file from that entry
              (dtd_module_uoa) - if specified use DTD file from that entry, otherwise 'xml'
              dtd_file   - DTD file
              xml_file   - XML file to be validated
            }

    Output: {
              return       - return code =  0, if successfully validated
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    from lxml import etree

    ocon=i.get('out','')=='con'

    # Checking entry with DTD if needed
    p=''
    duoa=i.get('data_uoa','')
    if duoa!='':
       muoa=i.get('dtd_module_uoa','')
       if muoa=='': muoa=i.get('module_uoa','')

       r=ck.access({'action':'load',
                    'module_uoa':muoa,
                    'data_uoa':duoa})
       if r['return']>0: return r

       p=r['path']

    # Checking DTD file
    dtd_file=i.get('dtd_file','')
    if dtd_file=='': 
       return {'return':1, 'error':'"dtd_file" is not specified'}

    if p!='':
       dtd_file=os.path.join(p, dtd_file)

    if not os.path.isfile(dtd_file):
       return {'return':1, 'error':'DTD file not found ('+dtd_file+')'}

    xml_file=i.get('xml_file','')
    if xml_file=='': 
       return {'return':1, 'error':'"xml_file" is not specified'}

    if not os.path.isfile(xml_file):
       return {'return':1, 'error':'XML file not found ('+xml_file+')'}

    # Load DTD
    fdtd=open(dtd_file)
    DTD=etree.DTD(fdtd)

    # Load XML
    xml=etree.parse(xml_file)

    # Validate
    validated=DTD.validate(xml)
 
    fdtd.close()

    if not validated:
       return {'return':1, 'error':'XML was not validated:\n'+str(DTD.error_log.filter_from_errors())}

    if ocon:
       ck.out('XML files was successfully validated against DTD!')

    return {'return':0}
