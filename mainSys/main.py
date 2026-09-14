from server import instance
import runtime

if __name__ == "__main__":
    instance.run(transport="sse", host="0.0.0.0", port=8000)