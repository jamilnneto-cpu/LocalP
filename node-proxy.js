const http = require('http');
const httpProxy = require('http-proxy');

// Create a proxy server
const proxy = httpProxy.createProxyServer({
  target: 'http://target-site.com',
  changeOrigin: true,
  // Force HTTP/1.1
  agent: new http.Agent({ keepAlive: false }),
  headers: {
    // Remove proxy headers
    'Via': undefined,
    'X-Forwarded-For': undefined,
    'Forwarded': undefined
  }
});

// Listen on localhost:8888
const server = http.createServer((req, res) => {
  console.log(`Proxying request: ${req.url}`);
  proxy.web(req, res);
});

server.listen(8888, '127.0.0.1', () => {
  console.log('Proxy server listening on http://127.0.0.1:8888');
});

// Handle errors
proxy.on('error', (err, req, res) => {
  console.error('Proxy error:', err);
  res.writeHead(500);
  res.end('Proxy error');
});
