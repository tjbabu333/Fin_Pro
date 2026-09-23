# Movie Review Sentiment Analysis Service

A lightweight Python Flask microservice that analyzes movie review sentiment and generates pseudo ratings.

## Features

- **Sentiment Analysis**: Analyzes text sentiment using TextBlob
- **Rating Generation**: Converts sentiment to 1-5 star ratings
- **Health Monitoring**: Kubernetes-ready health checks
- **Admin Controls**: Toggle service health for failure simulation

## API Endpoints

### Core Functionality

#### `POST /analyze`
Analyzes review text and returns sentiment + rating.

**Request:**
```json
{
  "text": "This movie was absolutely amazing!"
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "score": 0.625,
  "confidence": "high", 
  "rating": 4.6,
  "timestamp": 1701234567.89,
  "text_length": 33,
  "processed_by": "textblob"
}
```

### Health & Monitoring

#### `GET /health`
Health check endpoint for Kubernetes and backend monitoring.

#### `GET /admin/status`
Detailed service status and capabilities.

#### `POST /admin/toggle-health`
Toggle service health for failure simulation.

## Rating Logic

- **Positive Sentiment**: 4.0-5.0 stars
- **Neutral Sentiment**: 2.5-3.5 stars  
- **Negative Sentiment**: 1.0-2.0 stars

Rating precision correlates with sentiment confidence.

## Environment Variables

- `MODEL_PORT`: Service port (default: 5000)

## Docker Usage

```bash
# Build
docker build -t model:1 .

# Run (internal service)
docker run -d --name model --network movie model:1

# Test
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"Great movie!"}' http://localhost:5000/analyze
```

## Integration

The service integrates with the Movie Review Backend:
- Backend calls `POST http://model:5000/analyze`
- Returns sentiment analysis + star rating
- Handles graceful degradation when model service is down

## Dependencies

- **Flask**: Web framework
- **TextBlob**: Sentiment analysis
- **NLTK**: Natural language processing
- **Gunicorn**: Production WSGI server (optional)

Built for microservices architecture and Kubernetes deployment. 