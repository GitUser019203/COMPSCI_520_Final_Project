package uma.javasmartshark;

import java.util.List;
import org.refactoringminer.api.GitHistoryRefactoringMiner;
import org.refactoringminer.api.Refactoring;
import org.refactoringminer.api.GitService;
import org.refactoringminer.api.RefactoringHandler;
import org.refactoringminer.rm1.GitHistoryRefactoringMinerImpl;
import org.refactoringminer.util.GitServiceImpl;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.File;
import java.io.IOException;
import java.io.LineNumberReader;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.eclipse.jgit.lib.Repository;

public class refminerUsingCloning {
    private static final String[] SMART_SHARK_2_0_ISSUE_TRACKED_VCS_SYSTEM_URLS = {"https://github.com/apache/ant-ivy","https://github.com/apache/archiva.git","https://github.com/apache/calcite.git","https://github.com/apache/cayenne.git","https://github.com/apache/commons-bcel.git","https://github.com/apache/commons-beanutils.git","https://github.com/apache/commons-codec.git","https://github.com/apache/commons-collections.git","https://github.com/apache/commons-compress.git","https://github.com/apache/commons-configuration.git","https://github.com/apache/commons-dbcp.git","https://github.com/apache/commons-digester.git","https://github.com/apache/commons-io.git","https://github.com/apache/commons-jcs.git","https://github.com/apache/commons-jexl.git","https://github.com/apache/commons-lang.git","https://github.com/apache/commons-math","https://github.com/apache/commons-net.git","https://github.com/apache/commons-scxml.git","https://github.com/apache/commons-validator.git","https://github.com/apache/commons-vfs.git","https://github.com/apache/deltaspike.git","https://github.com/apache/eagle.git","https://github.com/apache/giraph.git","https://github.com/apache/gora.git","https://github.com/apache/jspwiki.git","https://github.com/apache/knox.git","https://github.com/apache/kylin.git","https://github.com/apache/lens.git","https://github.com/apache/mahout","https://github.com/apache/manifoldcf.git","https://github.com/apache/nutch.git","https://github.com/apache/opennlp.git","https://github.com/apache/parquet-mr.git","https://github.com/apache/santuario-java.git","https://github.com/apache/systemml.git","https://github.com/apache/tika.git","https://github.com/apache/wss4j.git"};
    private static final String CMD = "cmd";
    private static final String BASH = "bash";
    private static final String SH = "sh";
    // Add ProcessBuilder for Bash to run script for directory removal 
    // Add Process Builder for Shell
    private static final ProcessBuilder workingDirWin = new ProcessBuilder(CMD, "/c", "cd");
    private static String vcsSystemURL = new String();
    private static String vcsSystemName = new String();
    private static String issueTitle = new String();
    private static String issueID = new String();
    private static int numCommitsWithRefactoring = 0;
    private static int numCommitsMined = 0;
    private static int currLineNo = 0;
    private static String outString = new String();
    private static List<String> listIssueTitles = new ArrayList<String>();
    private static List<String> listIssueIDs = new ArrayList<String>();
    private static LineNumberReader dataExtractor;
    private static LineNumberReader miningStateReader;
    private static BufferedWriter miningStateWriter;    
    private static BufferedWriter miningErrorWriter;
    private static BufferedWriter refactoringInfoWriter;
    private static GitHistoryRefactoringMiner miner = new GitHistoryRefactoringMinerImpl();
    private static HashSet<String> uniqueRevisionHashesWithRefactoring = new HashSet<String>();
    private static Repository repo;
    private static GitService gitService = new GitServiceImpl();
    public static void main(String[] args) {
        System.out.println("Working Directory = " + System.getProperty("user.dir"));
        
        try {   
            dataExtractor = new LineNumberReader(new FileReader("mongo_db_extract_refactoring_doc.txt"));
        } catch (FileNotFoundException ex) {
            Logger.getLogger(refminerUsingCloning.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        for(int i = 0; i < SMART_SHARK_2_0_ISSUE_TRACKED_VCS_SYSTEM_URLS.length; i++) {
            try {
                vcsSystemURL = SMART_SHARK_2_0_ISSUE_TRACKED_VCS_SYSTEM_URLS[i];
                vcsSystemName =  vcsSystemURL.substring(vcsSystemURL.lastIndexOf('/') + 1);
                
                refactoringInfoWriter = new BufferedWriter(new FileWriter(vcsSystemName + " refactorings"));
                repo = gitService.cloneIfNotExists(
                        "C:/SmartSHARK/Refactorings/temp " + vcsSystemName,
                        vcsSystemURL);
                
                String line;
                line = dataExtractor.readLine();
                while(line != null) {
                    if(line.contains("VCS System:")){
                        // If the line is about the VCS system
                         int index = line.indexOf("https://");
                         String URL = line.substring(index);
                         if(!URL.equals(vcsSystemURL)) {
                             break;
                         }
                    } else if(line.contains("Linked Commit Github URL:")) {
                        // If the line is about a linked commit's GitHub URL
                        int index = line.indexOf("https://");
                        String URL = line.substring(index);
                        String revHash = URL.substring(URL.lastIndexOf("/") + 1);
                        mineCommit(revHash);
                    } else if(line.contains("Issue Id:")) {
                        // If the line is about an issue Id
                        int index = line.indexOf(": ");
                        issueID = line.substring(index);
                    } else if(line.contains("Issue Title:")) {
                        // If the line is about an issue title
                        int index = line.indexOf(": ");
                        issueTitle = line.substring(index);
                    }
                    line = dataExtractor.readLine();
                }
            } catch (Exception ex) {
                Logger.getLogger(Refminer.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        
    }
    
    private static void mineCommit(String revHash) {
        // Mine the commit revHash in the VCS system vcsSystemURL with a timeout of 60s
        miner.detectAtCommit(repo, revHash, new RefactoringHandler() {
            @Override
            public void handle(String commitId, List<Refactoring> refactorings) {
                numCommitsMined += 1;
                System.out.println("Already mined " + String.valueOf(numCommitsMined) + "/13,596 commits.");
                if(refactorings.size() > 0) {
                    outString += "VCS System: " + vcsSystemURL + "\n";
                    System.out.println("VCS System: " + vcsSystemURL);

                    if(!listIssueTitles.contains(issueTitle)) {
                        listIssueTitles.add(issueTitle);
                        outString += "Issue Title: " + issueTitle + "\n";
                        System.out.println("Issue Title: " + issueTitle);
                    } else {
                        listIssueTitles.add(issueTitle + " with ID " + issueID);
                        outString += "Issue Title: " + issueTitle + " with ID " + issueID + "\n";
                        System.out.println("Issue Title: " + issueTitle + " with ID " + issueID  );
                    }

                    outString += "Issue ID: " + issueID + "\n";
                    System.out.println("Issue ID: " + issueID);
                    listIssueIDs.add(issueID);

                    outString += "Refactorings at " + commitId + "\n";
                    System.out.println("Refactorings at " + commitId);

                    for (Refactoring ref : refactorings) {
                        outString += ref.toString() + "\n";
                        System.out.println(ref.toString());


                    }
                    numCommitsWithRefactoring += 1;
                    uniqueRevisionHashesWithRefactoring.add(commitId);
                    System.out.println("Number of commits with refactoring: " + String.valueOf(numCommitsWithRefactoring) + "/10708");
                    System.out.println("There are " + String.valueOf(numCommitsWithRefactoring - uniqueRevisionHashesWithRefactoring.size() + 1) + " duplicate commits with refactoring.");
                    
                }
            }
        }, 60);
    }
}