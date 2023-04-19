package uma.mavenproject1;

import java.util.List;
import java.util.ArrayList;
import org.refactoringminer.api.GitHistoryRefactoringMiner;
import org.refactoringminer.api.Refactoring;
import org.refactoringminer.api.RefactoringHandler;
import org.refactoringminer.rm1.GitHistoryRefactoringMinerImpl;
import java.io.BufferedReader;
import java.io.LineNumberReader;
import java.io.BufferedWriter;
import java.io.RandomAccessFile;
import java.io.File;
import java.io.FileWriter;
import java.io.FileReader;
import java.io.IOException;
import java.text.DateFormat;  
import java.text.SimpleDateFormat;  
import java.util.Date;  
import java.util.Calendar;  
import java.util.logging.Level;
import java.util.logging.Logger;

public class refMiner {
                
    static String vcsSystemUrl = new String();
    static String issueTitle = new String();
    static int numRefactoringCommmits = 0;
    static int numRequestsMade = 0;
    static int currLineNo = 0;
    static String out = new String();
    static List<String> listIssues = new ArrayList<String>();
    public static void main(String[] args) {
        System.out.println("Working Directory = " + System.getProperty("user.dir"));
        LineNumberReader reader;
        LineNumberReader stateReader;
        BufferedWriter writer;
        GitHistoryRefactoringMiner miner = new GitHistoryRefactoringMinerImpl();
        try {
            stateReader = new LineNumberReader(new FileReader("currState"));
            currLineNo = Integer.parseInt(stateReader.readLine().trim());
            vcsSystemUrl = stateReader.readLine().trim();
            issueTitle = stateReader.readLine().trim();
            numRefactoringCommmits = Integer.parseInt(stateReader.readLine().trim());
            
            String issues = stateReader.readLine();
            issues = issues.substring(1);
            issues = issues.substring(0, issues.length() - 1);
            String[] issuesArray = issues.split(",");
            for(int i = 0; i < issuesArray.length; i++) {
                listIssues.add(issuesArray[i]);
            }
            
            reader = new LineNumberReader(new FileReader("input"));
            
            String line = new String();
            
            for(int i = 0; i < currLineNo; i++) {
                line = reader.readLine();
            }

            Date date = Calendar.getInstance().getTime();  
            DateFormat dateFormat = new SimpleDateFormat("yyyy-mm-dd hh:mm:ss");  
            String strDate = dateFormat.format(date);    
            out += "Current date is: " + strDate + "\n";
            while (line != null && numRequestsMade <= 5000) {                    
                    if(line.contains("VCS System:")) {
                        int index = line.indexOf("https://");
                        
                        vcsSystemUrl = line.substring(index);
                        
                    }
                    
                    if(line.contains("Issue Title:")) {
                        int index = line.indexOf(": ");
                        issueTitle = line.substring(index);
                        
                    }
                    
                    
                    if(line.contains("Linked Commit Github URL:")) {
                        int index = line.indexOf("https://");
                        String url = line.substring(index);
                        String revHash = url.substring(url.lastIndexOf("/") + 1);
                        try {
                            //Ref: https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/rate-limits-for-oauth-apps
                            Thread.sleep(1000);
                            miner.detectAtCommit(vcsSystemUrl,
                            revHash, new RefactoringHandler() {
                              @Override
                              public void handle(String commitId, List<Refactoring> refactorings) {
                                numRequestsMade += 1;
                                if(refactorings.size() > 0) {
                                    out += "VCS System: " + vcsSystemUrl + "\n";
                                    System.out.println("VCS System: " + vcsSystemUrl);
                                    
                                    out += "Issue Title: " + issueTitle + "\n";
                                    System.out.println("Issue Title: " + issueTitle);
                                  
                                    if(!listIssues.contains(issueTitle)) {
                                        listIssues.add(issueTitle);
                                    }
                                    out += "Refactorings at " + commitId + "\n";
                                    System.out.println("Refactorings at " + commitId);
                                    
                                    for (Refactoring ref : refactorings) {
                                        out += ref.toString() + "\n";
                                        System.out.println(ref.toString());
                                        numRefactoringCommmits += 1;

                                    }
                                }
                              }
                            }, 10);
                        } catch (InterruptedException ex) {
                            Logger.getLogger(refMiner.class.getName()).log(Level.SEVERE, null, ex);
                        }
                        
                    }
                    // read next line
                    line = reader.readLine();
            }
            
            currLineNo = reader.getLineNumber();
            reader.close();
            System.out.println("There are " + numRefactoringCommmits + " refactoring commits linked to issues documenting the refactoring.");
            System.out.println("There are " + listIssues.size() + " refactoring related issues.");
            
            try {       
                    writer = new BufferedWriter(new FileWriter("currState"), 'w');
                    writer.write(String.valueOf(currLineNo) + "\n");
                    writer.write(vcsSystemUrl + "\n");
                    writer.write(issueTitle + "\n");
                    writer.write(numRefactoringCommmits + "\n");
                    writer.write(listIssues.toString() + "\n");
                    writer.close();
            } catch (IOException e) {       
                    e.printStackTrace();
            }
            
            try {       
                    writer = new BufferedWriter(new FileWriter("output", true));
                    writer.write(out);
                    writer.close();
            } catch (IOException e) {       
                    e.printStackTrace();
            }
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
