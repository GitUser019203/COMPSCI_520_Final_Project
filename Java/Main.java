package org.refactoringissuesminer;

import java.util.List;
import org.refactoringminer.api.GitHistoryRefactoringMiner;
import org.refactoringminer.api.Refactoring;
import org.refactoringminer.api.GitService;
import org.refactoringminer.api.RefactoringHandler;
import org.refactoringminer.rm1.GitHistoryRefactoringMinerImpl;
import org.refactoringminer.util.GitServiceImpl;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.LineNumberReader;
import java.util.HashSet;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.eclipse.jgit.lib.Repository;

public class Main {
    private static final String[] SMART_SHARK_2_0_ISSUE_TRACKED_VCS_SYSTEM_URLS = {"https://github.com/apache/ant-ivy","https://github.com/apache/archiva.git","https://github.com/apache/calcite.git","https://github.com/apache/cayenne.git","https://github.com/apache/commons-bcel.git","https://github.com/apache/commons-beanutils.git","https://github.com/apache/commons-codec.git","https://github.com/apache/commons-collections.git","https://github.com/apache/commons-compress.git","https://github.com/apache/commons-configuration.git","https://github.com/apache/commons-dbcp.git","https://github.com/apache/commons-digester.git","https://github.com/apache/commons-io.git","https://github.com/apache/commons-jcs.git","https://github.com/apache/commons-jexl.git","https://github.com/apache/commons-lang.git","https://github.com/apache/commons-math","https://github.com/apache/commons-net.git","https://github.com/apache/commons-scxml.git","https://github.com/apache/commons-validator.git","https://github.com/apache/commons-vfs.git","https://github.com/apache/deltaspike.git","https://github.com/apache/eagle.git","https://github.com/apache/giraph.git","https://github.com/apache/gora.git","https://github.com/apache/jspwiki.git","https://github.com/apache/knox.git","https://github.com/apache/kylin.git","https://github.com/apache/lens.git","https://github.com/apache/mahout","https://github.com/apache/manifoldcf.git","https://github.com/apache/nutch.git","https://github.com/apache/opennlp.git","https://github.com/apache/parquet-mr.git","https://github.com/apache/santuario-java.git","https://github.com/apache/systemml.git","https://github.com/apache/tika.git","https://github.com/apache/wss4j.git"};
    private static String vcsSystemURL = new String();
    private static String vcsSystemName = new String();
    private static String issueTitle = new String();
    private static String issueID = new String();
    private static int numCommitsWithRefactoring = 0;
    private static int numCommitsMined = 0;
    private static LineNumberReader dataExtractor;
    private static BufferedWriter refactoringInfoWriter;
    private static GitHistoryRefactoringMiner miner = new GitHistoryRefactoringMinerImpl();
    private static HashSet<String> uniqueRevisionHashesWithRefactoring = new HashSet<String>();
    private static Repository repo;
    private static GitService gitService = new GitServiceImpl();
    public static void main(String[] args) {
        // Print out the working directory where the input file is and the refactoring information is to be stored.
        System.out.println("Working Directory = " + System.getProperty("user.dir"));

        // Open the input file
        openDataFile();

        for(int i = 0; i < SMART_SHARK_2_0_ISSUE_TRACKED_VCS_SYSTEM_URLS.length; i++) {
            try {
                vcsSystemURL = SMART_SHARK_2_0_ISSUE_TRACKED_VCS_SYSTEM_URLS[i];
                vcsSystemName =  vcsSystemURL.substring(vcsSystemURL.lastIndexOf('/') + 1);

                File refactoringDataFile = new File("C:/SmartSHARK/RefactoringMiner/detectedRefactorings/" + vcsSystemName + ".refactorings");
                refactoringDataFile.createNewFile();
                refactoringInfoWriter = new BufferedWriter(new FileWriter(refactoringDataFile, true));
                repo = gitService.cloneIfNotExists(
                        "C:/SmartSHARK/RefactoringMiner/repos/" + vcsSystemName,
                        vcsSystemURL);

                String line;
                line = dataExtractor.readLine();
                while(line != null) {
                    System.out.println("Currently parsing line " + String.valueOf(dataExtractor.getLineNumber() - 1));
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

                    // Read the next line
                    line = dataExtractor.readLine();
                }
                refactoringInfoWriter.close();
            } catch (Exception ex) {
                Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, ex);
            }
        }

    }

    private static void openDataFile() {
        try {
            dataExtractor = new LineNumberReader(new FileReader("mongo_db_extract_refactoring_doc.txt"));
        } catch (FileNotFoundException ex) {
            Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    private static void mineCommit(String revHash) {
        // Mine the commit revHash in the VCS system vcsSystemURL with a timeout of 60s
        miner.detectAtCommit(repo, revHash, new RefactoringHandler() {
            @Override
            public void handle(String commitId, List<Refactoring> refactorings) {
                String outputString = new String();
                System.out.println("\nAlready mined " + String.valueOf(numCommitsMined) + "/13,596 commits.");
                if(refactorings.size() > 0) {
                    outputString += "VCS System: " + vcsSystemURL + "\n";
                    System.out.println("VCS System: " + vcsSystemURL);
                    outputString += "Issue ID: " + issueID + "\n";
                    System.out.println("Issue ID: " + issueID);
                    outputString += "Issue Title: " + issueTitle + "\n";
                    System.out.println("Issue Title: " + issueTitle);
                    outputString += "Refactorings at " + commitId + "\n";
                    System.out.println("Refactorings at " + commitId);
                    for (Refactoring ref : refactorings) {
                        outputString += ref.toString() + "\n";
                        System.out.println(ref.toString());
                    }
                    numCommitsWithRefactoring += 1;
                    uniqueRevisionHashesWithRefactoring.add(commitId);
                    outputString += "Developers have reported that 10708 commits involve refactoring but only " + String.valueOf(numCommitsWithRefactoring) + " involve refactoring operations" + "\n";
                    System.out.println("Developers have reported that 10708 commits involve refactoring but only " + String.valueOf(numCommitsWithRefactoring) + " involve refactoring operations");
                    outputString += "There are " + String.valueOf(numCommitsWithRefactoring - uniqueRevisionHashesWithRefactoring.size()) + " duplicate commits with refactoring out of the " + String.valueOf(numCommitsWithRefactoring) + " commits." + "\n\n";
                    System.out.println("There are " + String.valueOf(numCommitsWithRefactoring - uniqueRevisionHashesWithRefactoring.size()) + " duplicate commits with refactoring out of the " + String.valueOf(numCommitsWithRefactoring) + " commits.\n");
                } else {
                    outputString += "No refactorings detected at " + commitId + "\n\n";
                    System.out.println("No refactorings detected at " + commitId + "\n");
                }

                try {
                    refactoringInfoWriter.write(outputString);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
                numCommitsMined += 1;
            }
        }, 360);
    }
}