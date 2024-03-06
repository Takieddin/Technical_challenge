## API Documentation

Below you'll find detailed documentation for each endpoint, including example requests and responses to help you get started.

### General API Information

- Base URL: `http://<your-api-host>/` 
- All endpoints return either a JSON object or array.
- Data is sent and received as JSON.

### Endpoints

#### Get Index

- **URL**: `/`
- **Method**: `GET`
- **Description**: Retrieves the API index.
- **Example Request**: `curl -X GET "http://<your-api-host>/"`
- **Example Response**: `{"message": "Welcome to the Custom title API"}`

#### Create Image

- **URL**: `/images`
- **Method**: `POST`
- **Description**: Uploads a new image and creates an entry in the database.
- **Parameters**: Optional query parameters include `keep_aspect_ratio` (boolean) and `resize_width` (integer).
- **Example Request**: `curl -X POST "http://<your-api-host>/images?keep_aspect_ratio=true&resize_width=150" -F "file=@path/to/image.jpg"`
- **Example Response**: `{"message": "Image uploaded successfully"}`

#### Get Images

- **URL**: `/images`
- **Method**: `GET`
- **Description**: Retrieves a list of all images.
- **Example Request**: `curl -X GET "http://<your-api-host>/images"`
- **Example Response**: `{"images": [{"id": 1, "name": "Image 1"}, {"id": 2, "name": "Image 2"}]}`

#### Delete Image

- **URL**: `/images/{image_id}`
- **Method**: `DELETE`
- **Description**: Deletes a specific image by ID.
- **Parameters**: `image_id` (required path parameter).
- **Example Request**: `curl -X DELETE "http://<your-api-host>/images/1"`
- **Example Response**: `{"message": "Image deleted successfully"}`

#### Get Image Frame

- **URL**: `/images/{image_id}`
- **Method**: `GET`
- **Description**: Retrieves a specific image frame based on depth range and optional color map application.
- **Parameters**: `image_id` (required path parameter), `depth_min` and `depth_max` (optional query parameters), and `apply_color_map` (optional query parameter).
- **Example Request**: `curl -X GET "http://<your-api-host>/images/1?depth_min=10&depth_max=50&apply_color_map=true"`
- **Example Response**: `{"frame": "data:image/png;base64,..."}`

## Development To-Do List

- **Implement Authentication**: Add authentication to secure the API endpoints.
- **Use DataBase Server**: such as RDS.
- **Refactor Code**: Review and refactor code for efficiency and maintainability.
- **Setup CI/CD Pipeline**: Establish a CI/CD pipeline for automated testing and deployment.
- **Evaluate Serverless Options**: Consider serverless architectures, such as AWS Lambda and S3, for cost-effective scaling.
- **Deployment on EKS**: Deploy the application on Amazon EKS (Elastic Kubernetes Service) to leverage Kubernetes for scalability and management.
# Technical_challenge
# Technical_challenge
