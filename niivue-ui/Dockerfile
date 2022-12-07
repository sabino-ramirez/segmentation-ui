FROM node:16-alpine as builder
WORKDIR /app/niivue-ui
EXPOSE 3000
COPY . .
RUN npm install
ENTRYPOINT ["npm", "run", "dev"]
# ENTRYPOINT ["cat", "package.json"]
