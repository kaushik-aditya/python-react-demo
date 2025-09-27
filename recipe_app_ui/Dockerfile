# Dockerfile.dev
FROM node:22-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source
COPY . .

# Expose Vite's dev server port
EXPOSE 5173

# Run Vite dev server on container start
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
