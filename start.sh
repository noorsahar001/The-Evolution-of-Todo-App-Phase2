#!/bin/bash

# Backend start
cd backend
npm install
npm run start  # ya node index.js, jo aapka backend start karta hai

# Optional: frontend build
cd ../frontend
npm install
npm run build
