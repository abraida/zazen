const config = {
    development: {
        flaskUrl: 'http://localhost:5000',
    },
    production: {
        flaskUrl: 'https://.com',
    }
};

const currentEnv = process.env.NODE_ENV || 'development';
export default config[currentEnv];
