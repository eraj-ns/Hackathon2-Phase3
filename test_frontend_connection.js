// Test script to simulate frontend API connection
const axios = require('axios');

// Test API connection
async function testConnection() {
  try {
    console.log('Testing connection to backend...');

    // Test basic API endpoint
    const response = await axios.get('http://localhost:8000/');
    console.log('✓ Basic API connection successful:', response.data);

    // Test auth endpoint
    try {
      const authResponse = await axios.post('http://localhost:8000/auth/signin',
        new URLSearchParams({
          username: 'dua35347@gmail.com',
          password: 'password123'
        }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          }
        }
      );
      console.log('✓ Signin attempt completed:', authResponse.data);
    } catch (signinError) {
      if (signinError.response) {
        // Server responded with error status
        console.log('✗ Signin failed with status:', signinError.response.status, signinError.response.data);
      } else if (signinError.request) {
        // Request was made but no response received
        console.log('✗ Failed to fetch - no response received:', signinError.message);
      } else {
        // Something else happened
        console.log('✗ Error in request setup:', signinError.message);
      }
    }
  } catch (error) {
    console.log('✗ Connection test failed:', error.message);
  }
}

testConnection();