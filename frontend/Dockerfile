FROM node:20-bullseye-slim

WORKDIR /src

COPY package*.json ./

RUN npm install

COPY . .

# Expose port (if necessary)
EXPOSE 3000

CMD [ "npm", "run", "dev" ]
