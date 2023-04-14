package uma.smartshark.smartshark;

import java.util.List;
import java.util.ArrayList;
import org.refactoringminer.api.GitHistoryRefactoringMiner;
import org.refactoringminer.api.Refactoring;
import org.refactoringminer.api.RefactoringHandler;
import org.refactoringminer.rm1.GitHistoryRefactoringMinerImpl;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.FileReader;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class refminer {
                
    static String vcsSystemUrl = new String();
    static String issueTitle = new String();
    static int numRefactoringCommmits = 0;
    static int numRefactoringIssues = 0;
    static List<String> listIssues = new ArrayList<String>();
    public static void main(String[] args) {
        System.out.println("Working Directory = " + System.getProperty("user.dir"));
        BufferedReader reader;
        BufferedWriter writer;
        GitHistoryRefactoringMiner miner = new GitHistoryRefactoringMinerImpl();
        try {
            reader = new BufferedReader(new FileReader("input"));
            writer = new BufferedWriter(new FileWriter("output"));
            
            String line = reader.readLine();

            while (line != null) {                    
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
                            Thread.sleep(5000);
                            miner.detectAtCommit(vcsSystemUrl,
                            revHash, new RefactoringHandler() {
                              @Override
                              public void handle(String commitId, List<Refactoring> refactorings) {
                                if(refactorings.size() > 0) {
                                    System.out.println("VCS System: " + vcsSystemUrl);
                                    System.out.println("Issue Title: " + issueTitle);
                                    if(!listIssues.contains(issueTitle)) {
                                        listIssues.add(issueTitle);
                                    }
                                    System.out.println("Refactorings at " + commitId);
                                    
                                    for (Refactoring ref : refactorings) {
                                        System.out.println(ref.toString());
                                        numRefactoringCommmits += 1;


                                    }
                                }
                              }
                            }, 10);
                        } catch (InterruptedException ex) {
                            Logger.getLogger(refminer.class.getName()).log(Level.SEVERE, null, ex);
                        }
                        
                    }
                    // read next line
                    line = reader.readLine();
            }

            reader.close();
            System.out.println("There are " + numRefactoringCommmits + " refactoring commits linked to issues documenting the refactoring.");
            System.out.println("There are " + listIssues.size() + " refactoring related issues.");
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
