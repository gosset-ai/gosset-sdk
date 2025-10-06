"""
Command-line interface for Gosset SDK
"""
import sys
import argparse
import os

from .auth import get_oauth_token
from . import __version__


def get_token_command(args):
    """Handle 'get-token' command"""
    api_token = args.api_token or os.environ.get("GOSSET_API_TOKEN")
    
    if not api_token and not args.quiet:
        print("Note: No GOSSET_API_TOKEN set. You'll need to log in through the browser.")
        print("Alternatively, set GOSSET_API_TOKEN to authenticate automatically.")
        print()
    
    token = get_oauth_token(
        api_token=api_token,
        base_url=args.base_url,
        quiet=args.quiet
    )
    
    if token:
        if args.quiet:
            print(token)
        return 0
    else:
        return 1


def version_command(args):
    """Handle 'version' command"""
    print(f"Gosset SDK v{__version__}")
    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Gosset SDK - Command-line interface for Gosset Drug Database",
        prog="gosset"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # get-token command
    token_parser = subparsers.add_parser(
        "get-token",
        help="Get OAuth token for Gosset API"
    )
    token_parser.add_argument(
        "--api-token",
        help="GOSSET_API_TOKEN for authentication (optional)"
    )
    token_parser.add_argument(
        "--base-url",
        help="Custom API base URL (optional)"
    )
    token_parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only output the token (no additional messages)"
    )
    token_parser.set_defaults(func=get_token_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

