import { Command } from "commander";

interface OptionsObject {
  bytes?: boolean;
  chars?: boolean;
  lines?: boolean;
  "max-line-length"?: boolean;
  words?: boolean;
}
interface WCOutputInterface {
  filename: string;
  bytes: number;
  chars: number;
  lines: number;
  "max-line-length": number;
  words: number;
}

const program = new Command();
program
  .option("-c, --bytes", "print the byte counts")
  .option("-m, --chars", "print the character counts")
  .option("-l, --lines", "print the newline counts")
  .option("-L, --max-line-length", "print the maximum display width")
  .option("-w, --words", "print the word counts");

program.parse(Bun.argv);

let filenames: Array<string> = [];
for (let arg of Bun.argv.slice(2)) {
  if (!arg.startsWith("-")) {
    filenames.push(arg);
  }
}

const options: OptionsObject = program.opts();

if (Object.keys(options).length == 0) {
  // Just so that we don't repeat this declaration twice.
  options.bytes = true;
  options.chars = true;
  options.lines = true;
}

const fileproperties: Array<WCOutputInterface> = [];

// Some clarity, we will always give priority to
for (let file of filenames) {
  const tempfileoutput: WCOutputInterface = {
    filename: file,
    lines: -1,
    bytes: 0,
    words: 0,
    chars: 0,
    "max-line-length": 0,
  };
  try {
    const fpointer = Bun.file(file);
    if (await fpointer.exists()) {
      tempfileoutput.bytes = fpointer.size;
      const text = await fpointer.text();
      tempfileoutput.chars += text.length;
      for (let line of text.split("\n")) {
          tempfileoutput.lines+=1;
          if (line.length > tempfileoutput["max-line-length"]){
              tempfileoutput["max-line-length"] = line.length;
            }
        tempfileoutput.words += line.split(/\s|\t/).filter(w=>w!=="").length;

      }
      fileproperties.push(tempfileoutput);
    } else {
      throw new Error(`${file} does not exist`);
    }
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
}

console.log(fileproperties);