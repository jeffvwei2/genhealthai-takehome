# Build client
FROM node:20-alpine AS builder
WORKDIR /app
COPY client/package*.json client/
RUN cd client && npm ci
COPY client client
RUN cd client && npm run build

# Runtime
FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production

# Install server deps
COPY server/package*.json server/
RUN apk add --no-cache python3 make g++ \
  && cd server && npm ci --omit=dev

# Copy server and client build
COPY server server
COPY --from=builder /app/client/dist client/dist

EXPOSE 3001
CMD ["node", "server/index.js"]
