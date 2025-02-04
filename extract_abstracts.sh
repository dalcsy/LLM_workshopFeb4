grep "Abstract" Nature_Genetics_24.txt | sed 's/^Abstract: //' | awk 'NF >= 100'> Nature_genetics_24_abstracts_only.txt
grep "Abstract" American_Journal_of_Human_Genetics_24.txt | sed 's/^Abstract: //' | awk 'NF >= 100'> American_Journal_of_Human_Genetics_24_only.txt
