/**
 * @className: test
 * @author: Shidan Cheng
 * @description:
 * @date: 5:55 下午 2019/11/6
 * @version: v1.0
 */

import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.Node;
import org.dom4j.io.SAXReader;


import java.io.File;
import java.util.*;

public class test {
    public static void main(String[] args) {
        parse(new File("/Users/yagotoasa/Documents/Course/软件工程/K8s/github-repository/2019-XLab-KubernetesTools/XMLPraseTest/src/testXml.xml"));

    }

    public static void parse(File file) {
        try {
            SAXReader saxReader = new SAXReader();
            Document document = saxReader.read(file);
            Element root = document.getRootElement();
            Element dependenciesRootNode = root.element("dependencies");
            List dependencyList = dependenciesRootNode.elements("dependency");
            List<Map<String, Object>> depInfoList = new ArrayList<>();

            for (int i = 0; i < dependencyList.size(); i++) {
                Map<String, Object> info = new LinkedHashMap<>();
                Element dependency = (Element) dependencyList.get(i);
                parseAllChildrenNodes(info, (Element) dependency, null);
                Element exclusionsRootNode = dependency.element("exclusions");
                if (exclusionsRootNode != null) {
                    List exclusionList = exclusionsRootNode.elements("exclusion");
                    List<Map<String, Object>> excInfoList = new ArrayList<>();
                    for (int j = 0; j < exclusionList.size(); j++) {
                        Map<String, Object> excInfo = new LinkedHashMap<>();
                        Element exclusion = (Element) exclusionList.get(j);
                        parseAllChildrenNodes(excInfo, (Element) exclusion, null);
                        excInfoList.add(excInfo);
                    }
                    info.put("exclusions", excInfoList);
                }
                depInfoList.add(info);
            }
            depInfoList.forEach(System.out::println);
        } catch (DocumentException e) {
            e.printStackTrace();
        }
    }

    public static void parseAllChildrenNodes(Map<String, Object> info, Element node, Element fatherNode) {
        if (node.getName().equals("exclusions")) {
            return;
        }
        String nodeName = node.getName();
        String nodeValue = node.getTextTrim();
        if (!nodeValue.equals("")) {
            info.put(nodeName, nodeValue);
        }
        Iterator<Element> it = node.elementIterator();
        while (it.hasNext()) {
            Element e = it.next();
            parseAllChildrenNodes(info, e, node);
        }
    }
}
