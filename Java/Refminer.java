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
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.eclipse.jgit.lib.Repository;

public class Refminer {
    private static String vcsSystemUrl = new String();
    private static BufferedReader reader;
    private static BufferedWriter writer;
    private static final String[] SMART_SHARK_2_0_ISSUE_TRACKED_VCS_SYSTEM_URLS = {"https://github.com/apache/ant-ivy","https://github.com/apache/archiva.git","https://github.com/apache/calcite.git","https://github.com/apache/cayenne.git","https://github.com/apache/commons-bcel.git","https://github.com/apache/commons-beanutils.git","https://github.com/apache/commons-codec.git","https://github.com/apache/commons-collections.git","https://github.com/apache/commons-compress.git","https://github.com/apache/commons-configuration.git","https://github.com/apache/commons-dbcp.git","https://github.com/apache/commons-digester.git","https://github.com/apache/commons-io.git","https://github.com/apache/commons-jcs.git","https://github.com/apache/commons-jexl.git","https://github.com/apache/commons-lang.git","https://github.com/apache/commons-math","https://github.com/apache/commons-net.git","https://github.com/apache/commons-scxml.git","https://github.com/apache/commons-validator.git","https://github.com/apache/commons-vfs.git","https://github.com/apache/deltaspike.git","https://github.com/apache/eagle.git","https://github.com/apache/giraph.git","https://github.com/apache/gora.git","https://github.com/apache/jspwiki.git","https://github.com/apache/knox.git","https://github.com/apache/kylin.git","https://github.com/apache/lens.git","https://github.com/apache/mahout","https://github.com/apache/manifoldcf.git","https://github.com/apache/nutch.git","https://github.com/apache/opennlp.git","https://github.com/apache/parquet-mr.git","https://github.com/apache/santuario-java.git","https://github.com/apache/systemml.git","https://github.com/apache/tika.git","https://github.com/apache/wss4j.git"};
    private static final String CMD = "cmd";
    private static final String BASH = "bash";
    private static final String SH = "sh";
    // Add ProcessBuilder for Bash to run script for directory removal 
    // Add Process Builder for Shell
    private static final ProcessBuilder workingDirWin = new ProcessBuilder(CMD, "/c", "cd");
    public static void main(String[] args) {
        System.out.println("Working Directory = " + System.getProperty("user.dir"));
        GitHistoryRefactoringMiner miner = new GitHistoryRefactoringMinerImpl();
        GitService gitService = new GitServiceImpl();
        Repository repo;
        for(int i = 0; i < SMART_SHARK_2_0_ISSUE_TRACKED_VCS_SYSTEM_URLS.length; i++) {
            try {
                ProcessBuilder removeDirWin = new ProcessBuilder(CMD, "/c", "rmdir C:\\SmartSHARK\\Refactorings\\temp /q /s");
                removeDirWin.inheritIO();
                Process removeProcess = removeDirWin.start();
                try {
                    removeProcess.waitFor();
                } catch (InterruptedException ex) {
                    Logger.getLogger(Refminer.class.getName()).log(Level.SEVERE, null, ex);
                }
                
                String vcsSystemURL = SMART_SHARK_2_0_ISSUE_TRACKED_VCS_SYSTEM_URLS[i];
                String vcsSystemName =  vcsSystemURL.substring(vcsSystemURL.lastIndexOf('/') + 1);
                
                writer = new BufferedWriter(new FileWriter(vcsSystemName + " refactorings"));
                //https://stackoverflow.com/questions/8646517/how-can-i-see-the-size-of-a-github-repository-before-cloning-it
                //https://api.github.com/repos/apache/ant-ivy
                repo = gitService.cloneIfNotExists(
                        "C:/SmartSHARK/Refactorings/temp",
                        vcsSystemURL);
                try {
                    miner.detectAll(repo, "master", new RefactoringHandler() {
                        @Override
                        public void handle(String commitId, List<Refactoring> refactorings) {
                            System.out.println("Refactorings at " + commitId);
                            try {
                                writer.write("Refactorings at " + commitId + "\n");
                                for (Refactoring ref : refactorings) {
                                    System.out.println(ref.toString());
                                    writer.write(ref.toString() + "\n");
                                }
                            } catch (IOException ex) {
                                Logger.getLogger(Refminer.class.getName()).log(Level.SEVERE, null, ex);
                            }
                        }
                    });
                    
                    writer.close();
                } catch (Exception ex) {
                    Logger.getLogger(Refminer.class.getName()).log(Level.SEVERE, null, ex);
                }
            } catch (Exception ex) {
                Logger.getLogger(Refminer.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }
}
