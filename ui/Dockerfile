FROM node:18-alpine

ENV NODE_ENV development
WORKDIR /usr/src/app
COPY ["package.json", "package-lock.json*", "npm-shrinkwrap.json*", "yarn.lock", "./"]
RUN yarn
COPY . .
EXPOSE 5173
CMD ["yarn", "dev", "--host", "0.0.0.0"]