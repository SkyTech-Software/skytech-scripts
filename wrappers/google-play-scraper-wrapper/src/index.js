import gplay from "google-play-scraper";

// Get first argument from command line
let author = process.argv[2];

gplay.developer({devId: author, num: 200}).then(output_data).catch(err => {});

function output_data(data) {
  data.forEach((app) => {
    console.log(app["appId"]);
  });
}
