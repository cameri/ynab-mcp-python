import argparse


def main():
    parser = argparse.ArgumentParser(description="YNAB MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        required=True,
        help="The transport to use for communication.",
    )
    args = parser.parse_args()

    if args.transport == "stdio":
        print("Starting stdio transport...")
        # Placeholder for stdio logic
        pass
    elif args.transport == "http":
        print("Starting http transport...")
        # Placeholder for http logic
        pass


if __name__ == "__main__":
    main()
