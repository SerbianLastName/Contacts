FROM node:lts-alpine
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
RUN yarn global add @vue/cli -g
COPY package.json .
COPY package-lock.json .
RUN yarn install
CMD ["yarn", "run", "serve"]