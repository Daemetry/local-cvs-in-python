import argparse

help_parser = argparse.ArgumentParser(description="help ")

add_parser = argparse.ArgumentParser(description="help ")

commit_parser = argparse.ArgumentParser(description="commit")
commit_parser.add_argument("command_name")
commit_parser.add_argument('-m', "--message", metavar="Commit message",
                           dest="message", action="store",
                           help="The message, associated with commit",
                           required=True)

branch_parser = argparse.ArgumentParser(description="branch")
branch_parser.add_argument("command_name")
branch_parser.add_argument("name", metavar="Branch name", action="store",
                           help="The name of branch to be created",
                           )

tag_parser = argparse.ArgumentParser(description="branch")
tag_parser.add_argument("command_name")
tag_parser.add_argument("name", metavar="Tag name", action="store",
                        help="The name of tag to be created",
                        )

reset_parser = argparse.ArgumentParser(description="help ")

checkout_parser = argparse.ArgumentParser(description="help ")

log_parser = argparse.ArgumentParser(description="help ")
