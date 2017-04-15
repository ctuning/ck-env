import sys
import os

lib=sys.argv[1]

f=open(lib, 'r')
s=f.read()
f.close()

o ='/**********************************************************\n'
o+=' Automatically generated for Collective Knowledge Framework\n'
o+=' http://github.com/ctuning/ck\n'
o+='\n'
o+=' (C)opyright 2016 by Grigori Fursin (cTuning foundation)\n'
o+='\n'
o+=' Released under the same license as OpenCL\n'
o+=' (see include/CL/cl.h)\n'
o+='**********************************************************/\n'
o+='\n'
o+='#include <CL/cl.h>\n'
o+='\n'

ll=s.split('\n')

w=False
for l in ll:
    if w:
       if l.endswith(';'):
          w=False
          lx=l[:-1]+'\n'
          lx+='{}\n'
          lx+='\n'
       else:
          lx=l+'\n'

       # Process var names
       i1=lx.find('/*')
       if i1>0:
          i2=lx.find('*/',i1)
          if i2>0:
             vr=lx[i1+2:i2-1].strip()
             if vr.endswith('[3]'):
                vr=vr[:-3]
             lx=lx[:i1-1]+' '+vr+' '+lx[i2+2:]

       o+=lx

    elif l.startswith('extern CL_API_ENTRY ') and l.find('_DEPRECATED')<0:
       w=True
       o+=l[7:]+'\n'

# Write CK json
f=open('lib/stubs.c','wt')
f.write(o)
f.close()
