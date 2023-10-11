# Coding challenges - WC tool (Bun, Typescript)
## Requirements
BunJS needs to be installed

To install dependencies:

```bash
bun install
```

To run for dev purposes:

```bash
bun run prog [OPTIONS] [FILE]
```

There is also a standalone executable that you can build for your own platform using:

```bash
bun build --compile ccwc.ts --outfile=ccwc
```

Then you can run the commands similar to `wc` but substitute a `./ccwc` instead. 


This project was created using `bun init` in bun v1.0.4. [Bun](https://bun.sh) is a fast all-in-one JavaScript runtime.


**Status**
1. Character counts - complete
2. Line counts - Complete
3. Word counts - complete
4. Byte counts - complete
5. Pipe redirections - Complete

