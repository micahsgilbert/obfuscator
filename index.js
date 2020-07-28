let httpProxy = require("http-proxy")
let obfuscate = require("./obfuscation")
const fs = require("fs")

const TARGET = process.env.TARGET
const PORT = process.env.PORT || 9000

let proxy = httpProxy.createProxyServer({
  ssl: {
    key: fs.readFileSync("./cert/privkey.pem","utf8"),
    cert: fs.readFileSync("./cert/cert.pem","utf8")
  },
  target: TARGET,
  secure: false,
  selfHandleResponse: true,
  autoRewrite: true,
  hostRewrite: true,
  changeOrigin: true
})

proxy.on('proxyReq', (proxyReq, req, res) => {
  proxyReq.setHeader("Accept-Encoding", "identity")
})

proxy.on('proxyRes', (proxyRes, req, res) => {
  let body = []
  let contentType = proxyRes.headers["content-type"]

  if (proxyRes.statusCode == 301) { // gets url ending - otherwise running on port 9000 still redirects to standard port
    let urlPath = /(http[s]?:\/\/)?([^\/\s]+\/)(.*)/gm.exec(proxyRes.headers["location"])
    res.setHeader("Location","/" + urlPath[3])
    res.statusCode = 301
  }

  proxyRes.on("data", chunk => {
    body.push(chunk)
  })

  proxyRes.on("end", () => {
    let sess = /.*sess=(.*)/gm.exec(proxyRes.req.path)

    body = Buffer.concat(body).toString()
    obfuscate(body,contentType,sess,(obfuscated,err) => {
      if (err) {
        res.end(obfuscated)
      } else {
        let d = Buffer.from(obfuscated,"base64").toString()
        res.setHeader("Content-Type", contentType)
        res.end(d)
      }
    })
  })
})

proxy.listen(PORT)