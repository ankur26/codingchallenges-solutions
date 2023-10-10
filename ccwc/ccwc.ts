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

async function doWC(
  filenames: Array<string> = [],
  stdinOnly: boolean = false
): Promise<Array<WCOutputInterface>> {
  const fileproperties: Array<WCOutputInterface> = [];
  if (stdinOnly) {
    filenames = [""]; // Just substitute a dummy variable so that you don't
  }
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
      const stdinPointer = Bun.stdin;
      tempfileoutput.bytes = !stdinOnly ? fpointer.size : 0;
      let text = undefined
      
      if(!stdinOnly){
        text = await fpointer.exists() ? await fpointer.text() : text;
      }else{
        text = "";
        // text = text.concat(await Bun.readableStreamToText(stdinPointer.readable))
        for await(const chunk of stdinPointer.stream()){
            tempfileoutput.bytes += chunk.byteLength;
            text = text.concat(Buffer.from(chunk).toString());
        }
        // console.log(text)
      }
      if (text) {
        // console.log(text);
        tempfileoutput.chars += text.length;
        for (let line of text.split("\n")) {
          tempfileoutput.lines += 1;
          if (line.length > tempfileoutput["max-line-length"]) {
            tempfileoutput["max-line-length"] = line.length;
          }
          tempfileoutput.words += line
            .split(/\s|\t/)
            .filter((w) => w !== "").length;
        }
        fileproperties.push(tempfileoutput);
      }
    } catch (err) {
      console.error(err);
      process.exit(1);
    }
  }
  return fileproperties;
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
let fileproperties;
if (filenames.length == 0) {
  if (Bun.stdin) {
    // console.log("Waiting for stdin")
    // console.log(await Bun.stdin.text())
    fileproperties = await doWC([], true);
  } else {
    throw new Error("No input was received");
  }
} else {
  fileproperties = await doWC(filenames);
}
const options: OptionsObject = program.opts();

if (Object.keys(options).length == 0) {
  // Just so that we don't repeat this declaration twice.
  options.bytes = true;
  options.chars = true;
  options.lines = true;
}

for (let fileproperty of fileproperties) {
  // Not worry about space formatting inside the output, the correctness is more priority
  let consoleOutput = "\t";
  consoleOutput = options.lines
    ? consoleOutput.concat(`${fileproperty.lines}\t`)
    : consoleOutput;
  consoleOutput = options.words
    ? consoleOutput.concat(`${fileproperty.words}\t`)
    : consoleOutput;
  consoleOutput = options.chars
    ? consoleOutput.concat(`${fileproperty.chars}\t`)
    : consoleOutput;
  consoleOutput = options.bytes
    ? consoleOutput.concat(`${fileproperty.bytes}\t`)
    : consoleOutput;
  consoleOutput = options["max-line-length"]
    ? consoleOutput.concat(`${fileproperty["max-line-length"]}\t`)
    : consoleOutput;
  consoleOutput = consoleOutput.concat(`${fileproperty.filename}`);
  console.log(consoleOutput);
}
