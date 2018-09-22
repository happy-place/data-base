package com.big.data.logetl;

/*
-boOvAGNKUc     mrpitifulband   639     Music   287     7548    4.48    606     386     fmUwUURgsX0     bR27ACWomug     LlH7WcVptw8     saBmFpuwmKA     lhWk9SXUjWI     aVhSaa6aAOg     W-pvpxlOzZk        0vhVZQEzgcU     dDhCZVQf9po     zIkvMoezI1A     eV2SdBITv8k     cIO6nFDnNs4     Bd7nAtOEA3U     RZo5MisSTWo     geiABCqmQ84     MG1Xv99426g     7wj8-HkZ0XQ     JsdCu9T47iOUeN4DhCIFw      sf-Ym_pFP6U
 */

public class ETLUtil {
    public static String oriString2ETLString(String ori){
        StringBuilder etlString = new StringBuilder();
        String[] splits = ori.split("\t");
        if(splits.length < 9) return null;
        splits[3] = splits[3].replace(" ", "");
        for(int i = 0; i < splits.length; i++){
            if(i < 9){
                if(i == splits.length - 1){
                    etlString.append(splits[i]);
                }else{
                    etlString.append(splits[i] + "\t");
                }
            }else{
                if(i == splits.length - 1){
                    etlString.append(splits[i]);
                }else{
                    etlString.append(splits[i] + "&");
                }
            }
        }

        return etlString.toString();
    }
}
