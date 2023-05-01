package uma.javasmartshark;

import java.util.List;
import java.util.ArrayList;
import org.refactoringminer.api.GitHistoryRefactoringMiner;
import org.refactoringminer.api.Refactoring;
import org.refactoringminer.api.RefactoringHandler;
import org.refactoringminer.rm1.GitHistoryRefactoringMinerImpl;
import java.io.LineNumberReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.FileReader;
import java.io.IOException;
import java.text.DateFormat;  
import java.text.SimpleDateFormat;  
import java.util.Date;  
import java.util.HashSet;
import java.util.Calendar;  
import java.util.logging.Level;
import java.util.logging.Logger;

public class RefactoringMiner {
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
    public static void main(String[] args) {
        // Print out the current working directory
        System.out.println("Working Directory = " + System.getProperty("user.dir"));

        try {
            parseMiningState();
        } catch (IOException ex) {
            Logger.getLogger(RefactoringMiner.class.getName()).log(Level.SEVERE, null, ex);
        } catch (NumberFormatException ex) {
            Logger.getLogger(RefactoringMiner.class.getName()).log(Level.SEVERE, null, ex);
        }

        String line;
        try {
            line = seekNextLine();
            appendDateTime();

            // Repeatedly mine commits until EOF is encountered or at least 5000 commits have been mined
            while (line != null && numCommitsMined <= 5000) {                    
                parseVCSSystem(line);

                parseIssueTitle(line);

                parseIssueID(line);

                parseLinkedCommit(line);

                try {
                    // read next line
                    line = dataExtractor.readLine();
                } catch (IOException ex) {
                    Logger.getLogger(RefactoringMiner.class.getName()).log(Level.SEVERE, null, ex);
                }
                currLineNo = dataExtractor.getLineNumber();
            }
            closeReader();
        } catch (IOException ex) {
            Logger.getLogger(RefactoringMiner.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    private static void closeReader(){
        try {
            // Close the data extractor file
            dataExtractor.close();
        } catch (IOException ex) {
            Logger.getLogger(RefactoringMiner.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    private static void parseLinkedCommit(String line) {
        if(line.contains("Linked Commit Github URL:")) {
            // If the line is about a linked commit's GitHub URL
            int index = line.indexOf("https://");
            String URL = line.substring(index);
            String revHash = URL.substring(URL.lastIndexOf("/") + 1);
            try {
               
                // Sleep between commit mining to reduce the rate of requests
                //Ref: https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/rate-limits-for-oauth-apps
                Thread.sleep(1000);

                mineCommit(revHash);
                saveCurrentMiningState();
            } catch (Exception ex) {
                try {
                    miningErrorWriter = new BufferedWriter(new FileWriter("Mined Refactorings\\" + vcsSystemName + ".errors", true));
                } catch (IOException ex1) {
                    Logger.getLogger(RefactoringMiner.class.getName()).log(Level.SEVERE, null, ex1);
                }
                String errorInfo = "Revision Hash: " + revHash + "\n" + ex.toString();
                if(!errorInfo.contains("Rate")) {
                    try {
                        miningErrorWriter.write(errorInfo);
                    } catch (IOException ex1) {
                        Logger.getLogger(RefactoringMiner.class.getName()).log(Level.SEVERE, null, ex1);
                    }
                } else {
                    System.out.println(errorInfo);
                    try {
                        miningErrorWriter.write(errorInfo);
                    } catch (IOException ex1) {
                        Logger.getLogger(RefactoringMiner.class.getName()).log(Level.SEVERE, null, ex1);
                    }
                    System.exit(1);
                }
                try {
                    miningErrorWriter.close();
                } catch (IOException ex1) {
                    Logger.getLogger(RefactoringMiner.class.getName()).log(Level.SEVERE, null, ex1);
                }
            }
            
        }
    }

    private static void mineCommit(String revHash) {
        // Mine the commit revHash in the VCS system vcsSystemURL with a timeout of 60s
        miner.detectAtCommit(vcsSystemURL, revHash, new RefactoringHandler() {
            @Override
            public void handle(String commitId, List<Refactoring> refactorings) {
                numCommitsMined += 1;
                System.out.println("Already mined " + String.valueOf(numCommitsMined) + "/10708 commits.");
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
                    
                    saveRefactoringInformation();
                }
            }
        }, 60);
    }

    private static void saveCurrentMiningState() {
        try {
            // Write information about the current state of data extraction to currState
            miningStateWriter = new BufferedWriter(new FileWriter("currMiningState"), 'w');
            miningStateWriter.write(String.valueOf(currLineNo + 1) + "\n");
            miningStateWriter.write(vcsSystemURL + "\n");
            miningStateWriter.write(issueTitle + "\n");
            miningStateWriter.write(numCommitsWithRefactoring + "\n");
            miningStateWriter.write(numCommitsMined + "\n");
            miningStateWriter.write(listIssueTitles.toString() + "\n");            
            miningStateWriter.write(listIssueIDs.toString() + "\n");
            miningStateWriter.write(uniqueRevisionHashesWithRefactoring.toString() + "\n");
            miningStateWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void parseIssueTitle(String line) {
        if(line.contains("Issue Title:")) {
            // If the line is about an issue title
            int index = line.indexOf(": ");
            issueTitle = line.substring(index);
        }
    }

    private static void parseVCSSystem(String line) {
        if(line.contains("VCS System:")) {
            // If the line is about the VCS system
            int index = line.indexOf("https://");
            vcsSystemURL = line.substring(index);
            vcsSystemName = vcsSystemURL.substring(vcsSystemURL.lastIndexOf('/') + 1);
        }
    }

    private static void appendDateTime() {
        // Get the current data and time and append it to the ouptut string
        Date date = Calendar.getInstance().getTime();
        DateFormat dateFormat = new SimpleDateFormat("yyyy-mm-dd hh:mm:ss");
        String strDate = dateFormat.format(date);
        outString += "Current date is: " + strDate + "\n";
    }

    private static String seekNextLine() throws FileNotFoundException, IOException {
        // Open the file produced using Python
        dataExtractor = new LineNumberReader(new FileReader("mongo_db_extract_refactoring_doc.txt"));
        String line = new String();
        // Seek the next line to be read
        for(int i = 0; i < currLineNo; i++) {
            line = dataExtractor.readLine();
        }
        return line;
    }

    private static void parseMiningState() throws IOException, NumberFormatException, FileNotFoundException {
        // Parse the current mining state file
        miningStateReader = new LineNumberReader(new FileReader("currMiningState"));
        currLineNo = Integer.parseInt(miningStateReader.readLine().trim());
        vcsSystemURL = miningStateReader.readLine().trim();
        vcsSystemName = vcsSystemURL.substring(vcsSystemURL.lastIndexOf('/') + 1);
        issueTitle = miningStateReader.readLine().trim();
        numCommitsWithRefactoring = Integer.parseInt(miningStateReader.readLine().trim());
        numCommitsMined = Integer.parseInt(miningStateReader.readLine().trim());
        
        String issueTitles = miningStateReader.readLine();
        issueTitles = issueTitles.substring(1);
        issueTitles = issueTitles.substring(0, issueTitles.length() - 1);
        String[] issueTitlesArray = issueTitles.split(",");
        for(int i = 0; i < issueTitlesArray.length; i++) {
            listIssueTitles.add(issueTitlesArray[i]);
        }
        String issueIDs = miningStateReader.readLine();
        issueIDs = issueIDs.substring(1);
        issueIDs = issueIDs.substring(0, issueIDs.length() - 1);
        String[] issueIDsArray = issueIDs.split(",");
        for(int i = 0; i < issueIDsArray.length; i++) {
            listIssueIDs.add(issueIDsArray[i]);
        }
        
        String revHashes = miningStateReader.readLine();
        revHashes = revHashes.substring(1);
        revHashes = revHashes.substring(0, revHashes.length() - 1);
        String[] revHashesArray = revHashes.split(",");
        for(int i = 0; i < revHashesArray.length; i++) {
            uniqueRevisionHashesWithRefactoring.add(revHashesArray[i]);
        }
    }

    private static void parseIssueID(String line) {
        if(line.contains("Issue Id:")) {
            // If the line is about an issue title
            int index = line.indexOf(": ");
            issueID = line.substring(index);
        }
    }

    private static void saveRefactoringInformation() {
        try {
            // Open a buffered file writer in append mode
            refactoringInfoWriter = new BufferedWriter(new FileWriter("Mined Refactorings\\" + vcsSystemName, true));
            
            // Write the refactoring information to the file
            refactoringInfoWriter.write(outString);
            
            // Close the refactoringInfoWriter for the last VCS System mined.
            refactoringInfoWriter.close();
        } catch (IOException ex) {
            Logger.getLogger(RefactoringMiner.class.getName()).log(Level.SEVERE, null, ex);
        }

        outString = "";
    }
}