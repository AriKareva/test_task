FROM node:18-slim
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN chown -R node:node /app
USER node
CMD ["npm", "run", "dev", "--", "--host"]