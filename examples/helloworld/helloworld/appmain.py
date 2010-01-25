"""
This is the application's core code.  Unless you know the "ins-and-outs" of
The Cement CLI Application Framework, you probably should not modify this file.
Keeping all customizations outside of core.py means that you can easily 
upgrade to a newer version of the CEMENT_API by simply replacing this
file.
"""

import sys
from pkg_resources import get_distribution

from cement import namespaces
from cement.core.exc import CementArgumentError, CementConfigError, \
                            CementRuntimeError
from cement.core.log import get_logger
from cement.core.app_setup import lay_cement
from cement.core.configuration import ensure_api_compat
from cement.core.command import run_command

from helloworld import default_config

REQUIRED_CEMENT_API = '0.5-0.6:20100115'
VERSION = get_distribution('helloworld').version
BANNER = """
helloworld version %s, built on Cement (api:%s)
""" % (VERSION, REQUIRED_CEMENT_API)

def main():
    try:
        ensure_api_compat(__name__, REQUIRED_CEMENT_API)    
        lay_cement(config=default_config, banner=BANNER)
    
        log = get_logger(__name__)
        log.debug("Cement Framework Initialized!")
    
        # Setup the root controller
        from helloworld.controllers import root
        
        if not len(sys.argv) > 1:
            raise CementArgumentError, "A command is required. See --help?"
        
        run_command(sys.argv[1])
            
    except CementArgumentError, e:
        print("CementArgumentError > %s" % e)
        
        if namespaces['global'].config['debug']:
            import traceback
            traceback.print_stack()
        sys.exit(e.code)
    except CementConfigError, e:
        print("CementConfigError > %s" % e)
        if namespaces['global'].config['debug']:
            import traceback
            traceback.print_stack()
        sys.exit(e.code)
    except CementRuntimeError, e:
        print("CementRuntimeError > %s" % e)
        if namespaces['global'].config['debug']:
            import traceback
            traceback.print_exc()
        sys.exit(e.code)
    sys.exit(0)
        
if __name__ == '__main__':
    main()
    
