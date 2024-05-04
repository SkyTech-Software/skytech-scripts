import gplay from "google-play-scraper";

// Get first argument from command line
let author = process.argv[2];

let set = new Set();

async function get_data() {
  await gplay.developer({ devId: author, num: 200, country: 'pl' }).then(data => data.forEach(d => set.add(d["appId"]))).catch(e => { });
  await gplay.developer({ devId: author, num: 200, country: 'lt' }).then(data => data.forEach(d => set.add(d["appId"]))).catch(e => { });
  await gplay.developer({ devId: author, num: 200, country: 'lv' }).then(data => data.forEach(d => set.add(d["appId"]))).catch(e => { });
  await gplay.developer({ devId: author, num: 200, country: 'ee' }).then(data => data.forEach(d => set.add(d["appId"]))).catch(e => { });
  await gplay.developer({ devId: author, num: 200, country: 'cz' }).then(data => data.forEach(d => set.add(d["appId"]))).catch(e => { });
}

get_data().then(() => {
  for (let app of set) {
    console.log(app);
  }
});
