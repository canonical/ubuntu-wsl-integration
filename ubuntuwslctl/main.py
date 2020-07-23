import sys
import ubuntuwslctl.loader as loader
import ubuntuwslctl.helper as helper

def main():
    args = sys.argv[1:]
    if len(args) >= 1:
        if args[0] in ("help", "h"):
            print("ubuntuwslctl help placeholder")
            sys.exit()
        UbuntuWSLConfig = loader.UbuntuWSLConfigEditor()
        WSLConfig = loader.WSLConfigEditor()
        if args[0] in ("list", "ls"):
            UbuntuWSLConfig.list()
            WSLConfig.list()
        elif args[0] in ("show", "s"):
            try:
                config_type, config_section, config_setting = helper.config_name_extractor(args[1])
                if config_type == "":
                    print("Invalid config name. please check again.")
                    sys.exit(1)
                elif config_type == "Ubuntu":
                    UbuntuWSLConfig.show(config_section, config_setting)
                elif config_type == "WSL":
                    WSLConfig.show(config_section, config_setting)
            except KeyError:
                print("ERROR: Unknown keyname `" + args[1] + "` passed.")
                sys.exit(1)
            
        else:
            print("")
            # grewritingpool.helper._print_random_article(args[0])
    elif len(args) == 0:
        print("")
        # grewritingpool.helper._print_random_article()
    else:
        print("ubuntuwslctl")
        sys.exit(1)


if __name__ == '__main__':
    main()
