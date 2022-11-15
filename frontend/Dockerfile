FROM node:lts-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

# Allow user to write to node_modules
RUN chmod +w -R /app/node_modules

RUN npm install @vue/cli -g

COPY package.json .
COPY package-lock.json .
RUN npm install

CMD ["npm", "run", "serve"]