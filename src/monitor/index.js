const program = require("commander");
const mutasdk = require("muta-sdk");
const fs = require("fs");
const toml = require("toml");
const request = require("request-promise-native");
const child_process = require("child_process");

const { args } = program
    .option("-c --config [config]", "config", "../../res/config.toml")
    .option("-d --duration [duration]", "number of second", 300)
    .parse(process.argv);

const opts = program.opts();
const conf = toml.parse(fs.readFileSync(opts.config))

async function warn(text) {
    console.log(text);
    var ic = 0;
    while (text.length > ic) {
        await request.post({
            url: `https://api.telegram.org/bot${conf.telegram_token}/sendMessage`,
            form: {
                chat_id: conf.telegram_chat_id,
                text: text.substring(ic, ic + 4096),
            }
        });
        ic = ic + 4096;
    }
}

async function main() {
    const func = async () => {
        let text = "--- AWS Test ---\r\n"
        for await (const host of conf.aws_ip_node_list.concat(conf.aws_ip_sync_list)) {
            var sdk = new mutasdk.Muta({
                endpoint: "http://" + host + ":8000" + '/graphql',
            }).client();
            try {
                var res = await sdk.getLatestBlockHeight();
                text = text + host + " " + res;
            } catch (err) {
                console.log(err);
            }
            const stdout = child_process.execSync(`ssh -o "StrictHostKeyChecking no" -i ../../res/id_rsa ubuntu@${host} "free -h | head -n 2 | tail -n 1"`)
            text = text + " " + String(stdout).split(" ").filter(e => e !== "")[2];
            text = text + "\n";
        }
        warn(text)
    }
    func()
    setInterval(func, opts.duration * 1000);
}

main()
