const { spawn } = require("child_process")

module.exports = (body,contentType,sess,callback) => {

  let sessId = "null"

  if (sess) {
    sessId = sess[1]
  }

  const python = spawn('python3', ["/home/mgilbert/node-obfuscation/obfuscation/obfuscation.py", Buffer.from(body).toString("base64"), contentType, sessId])
  python.stdout.on('data', d => {
    callback(d.toString(), false)
  })
  python.stderr.on("data", d => {
    d = d.toString()
    console.log(d)
    callback(d, true)
  })
}