
# Image-Server

## Overview

Image-Server is a simplified, lightweight, and efficient image-serving API built using the FastAPI framework. The core purpose of this project is to serve images from a local directory into a gallery to easily browse through remote images in a nice convenient interface
## Features

- **Efficient Image Retrieval:** Fetch images swiftly from the specified local directory.
- **Dynamic Scaling:** Optionally resize images on-the-fly to cater to various device sizes and save bandwidth.
- **API Endpoints:** Utilize RESTful API endpoints to fetch and manipulate image data.

## Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn (or any ASGI server)

## Installation

Clone the repository:

```bash
git clone https://github.com/msalvaris/image-server.git
cd image-server
```

Install

```bash
pip install https://github.com/msalvaris/image-server.git
```

## Usage

### Running the Server

To run the server, use the following command:

```bash
image-server
```

Now, the API will be accessible at `http://127.0.0.1:8000`.

### API Endpoints
- **Get an Image from directory**
  - Endpoint: `/?images_dir={image_dir}`
  - Method: `GET`
  - Description: Fetch all images from directory
  - Example: `GET /?images_dir=images`

## Contributing

We welcome contributions to the Image-Server! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) for providing a superb, fast (high-performance) web framework to build APIs.
