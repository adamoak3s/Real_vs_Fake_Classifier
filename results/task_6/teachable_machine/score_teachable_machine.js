const tf = require('@tensorflow/tfjs');
const fs = require('fs'); const path = require('path'); const { PNG } = require('pngjs');
const [modelDir, imgDir, outCsv] = process.argv.slice(2);
(async () => {
  const mj = JSON.parse(fs.readFileSync(path.join(modelDir, 'model.json')));
  const buf = fs.readFileSync(path.join(modelDir, 'weights.bin'));
  const weightData = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
  const weightSpecs = mj.weightsManifest.flatMap(g => g.weights);
  const model = await tf.loadLayersModel({ load: async () => ({ modelTopology: mj.modelTopology, weightSpecs, weightData }) });
  const files = fs.readdirSync(imgDir).filter(f => f.endsWith('.png')).sort();
  const rows = ['id,p_class1,p_class2'];
  for (const f of files) {
    const png = PNG.sync.read(fs.readFileSync(path.join(imgDir, f)));
    const p = tf.tidy(() => {
      const rgba = tf.tensor3d(new Uint8Array(png.data), [png.height, png.width, 4]);
      const rgb = rgba.slice([0, 0, 0], [-1, -1, 3]).toFloat();
      const x = tf.image.resizeBilinear(rgb.expandDims(0), [224, 224]).div(127).sub(1);   // Teachable Machine's own preprocessing
      return model.predict(x).dataSync();
    });
    rows.push(`${parseInt(f.match(/(\d+)/)[1])},${p[0].toFixed(4)},${p[1].toFixed(4)}`);
  }
  fs.writeFileSync(outCsv, rows.join('\n') + '\n'); console.log('scored', files.length);
})();
