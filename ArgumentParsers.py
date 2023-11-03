import argparse


help_parser = argparse.ArgumentParser(description="help ")


add_parser = argparse.ArgumentParser(description="help ")


commit_parser = argparse.ArgumentParser(description="commit")
commit_parser.add_argument("command_name")
commit_parser.add_argument('-m', "--message", metavar="message",
                           dest="message", action="store",
                           help="The message, associated with commit",
                           required=True)


branch_parser = argparse.ArgumentParser(description="branch")
branch_parser.add_argument("command_name")
branch_parser.add_argument("name", metavar="Branch name", action="store",
                           help="The name of branch to be created")


tag_parser = argparse.ArgumentParser(description="branch")
tag_parser.add_argument("command_name")
tag_parser.add_argument("name", metavar="tag name", action="store",
                        help="The name of tag to be created")


reset_parser = argparse.ArgumentParser(description="help ")


checkout_parser = argparse.ArgumentParser(description="checkout")
checkout_parser.add_argument("command_name")
checkout_parser.add_argument("target", metavar="name/hash", action="store",
                             help="Hash of the commit or name of the branch/tag")
checkout_parser.add_argument('-f', "--force", action="store_true", dest="force",
                             help="if present, any indexed changes will be discarded")


merge_parser = argparse.ArgumentParser(description="merge")
merge_parser.add_argument("command_name")
merge_parser.add_argument("branch", metavar="name", action="store",
                          help="Branch that is going to be merged onto HEAD")


log_parser = argparse.ArgumentParser(description="help ")
