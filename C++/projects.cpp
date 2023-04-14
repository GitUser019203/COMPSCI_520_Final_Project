/******************************************************************************

                              Online C++ Compiler.
               Code, Compile, Run and Debug C++ program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <iostream>
#include <string>
#include <vector>
#include <sstream>
using namespace std;

int main()
{
    string projects = "activemq, ant-ivy, archiva, bigtop, calcite, cayenne, commons-bcel, commons-beanutils, commons-codec, commons-collections, commons-compress, commons-configuration, commons-dbcp, commons-digester, commons-imaging, commons-io, commons-jcs, commons-jexl, commons-lang, commons-math, commons-net, commons-scxml, commons-validator, commons-vfs, deltaspike, derby, directory-fortress-core, eagle, falcon, flume, giraph, gora, helix, httpcomponents-client, httpcomponents-core, jackrabbit, jena, jspwiki, knox, kylin, lens, mahout, manifoldcf, mina-sshd, nutch, oozie, opennlp, parquet-mr, pdfbox, phoenix, pig, ranger, roller, samza, santuario-java, storm, streams, struts, systemml, tez, tika, wss4j, xerces2-j zookeeper";
    string iss_tracked_projs_2_2 = "ant-ivy, archiva, calcite, cayenne, commons-bcel, commons-beanutils, commons-codec, commons-collections, commons-compress, commons-configuration, commons-dbcp, commons-digester,  commons-io, commons-jcs, commons-jexl, commons-lang, commons-math, commons-net, commons-scxml, commons-validator, commons-vfs, deltaspike, eagle, giraph, gora, jspwiki, knox, kylin, lens, mahout, manifoldcf, nutch, opennlp, parquet-mr, santuario-java, systemml, tika, wss4j";
    string iss_tracked_projs_2_0 = "ant-ivy,archiva,calcite,cayenne,commons-bcel,commons-beanutils,commons-codec,commons-collections,commons-compress,commons-configuration,commons-dbcp,commons-digester,commons-io,commons-jcs,commons-jexl,commons-lang,commons-math,commons-net,commons-scxml,commons-validator,commons-vfs,deltaspike,eagle,giraph,gora,jspwiki,knox,kylin,lens,mahout,manifoldcf,nutch,opennlp,parquet-mr,santuario-java,systemml,tika,wss4j";
    vector<string> v;

    stringstream ss1(projects);

    while (ss1.good()) {
        string substr;
        getline(ss1, substr, ',');
        v.push_back(substr);
    }

    cout << "num of projects in 2.0: " << v.size() << endl;

    for (size_t i = 0; i < v.size(); i++)
        cout << i << ":" << v[i] << endl;

    v.clear();

    stringstream ss2(iss_tracked_projs_2_2);

    while (ss2.good()) {
        string substr;
        getline(ss2, substr, ',');
        v.push_back(substr);
    }

    cout << "num of projects in 2.2 issue tracked: " << v.size() << endl;

    for (size_t i = 0; i < v.size(); i++)
        cout << i << ":" << v[i] << endl;

    v.clear();

    stringstream ss3(iss_tracked_projs_2_0);

    while (ss3.good()) {
        string substr;
        getline(ss3, substr, ',');
        v.push_back(substr);
    }

    cout << "num of projects in 2.0 issue tracked: " << v.size() << endl;

    for (size_t i = 0; i < v.size(); i++)
        cout << i << ":" << v[i] << endl;

    v.clear();
    return 0;
}
