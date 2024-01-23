package cccat;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.nio.file.Paths;
import java.util.Scanner;
import java.util.concurrent.Callable;

import picocli.CommandLine.Command;
import picocli.CommandLine.Option;
import picocli.CommandLine.Parameters;

@Command(name = "cccat", mixinStandardHelpOptions = true, version = "1.0", description = "The cat utThe cat utility reads files sequentially, writing them to the standard output.The file operands are processed in command-line order.  If file is a single dash ('-') or absent, cat reads from the standard input.")
public class CatClass implements Callable<Integer> {
        @Parameters(description = "File/s to output, leave blank or enter - if processing from standard input", defaultValue = Parameters.NULL_VALUE)
        private String[] filePaths;
        @Option(names = {
                        "-n", "--number-lines"
        }, description = "Number the lines including empty lines")
        private boolean includeBlankLineNumbers;
        @Option(names = {
                        "-b", "--no-blanks"
        }, description = "Don't include blanks while printing line numbers,")
        private boolean notIncludeBlankLineNumbers;

        private int lineNumber = 1;

        private String genStringWithLines(String str) {
                String out;
                if (includeBlankLineNumbers) {
                        out = String.format("%d %s", lineNumber,str);
                        lineNumber+=1;

                } else if (notIncludeBlankLineNumbers) {
                        if(str.equals("\n")|| str.isBlank() || str.isEmpty()){
                                out = str;
                        }else{
                                out = String.format("%d %s", lineNumber,str);
                                lineNumber+=1;
                        }
                }else{
                        out = str;
                }
                return out;
        }

        public Integer call() throws Exception {
                if (includeBlankLineNumbers && notIncludeBlankLineNumbers) {
                        System.out.println("Options -b and -n cannot be used at the same time");
                        return 1;
                }
                if (filePaths == null  || filePaths.length == 0) {
                        // System.out.println("WE have entered a null file");
                        Scanner scanner = new Scanner(System.in);
                        while (scanner.hasNextLine()) {
                                System.out.println(genStringWithLines(scanner.nextLine()));
                        }
                        scanner.close();
                } else {
                        // System.out.println("We have a file with us to read");
                        for (String filePath : filePaths) {
                                File file = Paths.get(System.getProperty("user.dir"), filePath).toFile();
                                BufferedReader br = new BufferedReader(new FileReader(file));
                                String line;
                                while ((line = br.readLine()) != null) {
                                        System.out.println(genStringWithLines(line));
                                }
                                br.close();
                        }
                }
                return 0;
        }
}
