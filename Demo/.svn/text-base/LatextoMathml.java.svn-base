/* $Id: BasicUpConversionExample.java 525 2010-01-05 14:07:36Z davemckain $
 *
 * Copyright (c) 2010, The University of Edinburgh.
 * All Rights Reserved
 */
import uk.ac.ed.ph.snuggletex.SnuggleEngine;
import uk.ac.ed.ph.snuggletex.SnuggleInput;
import uk.ac.ed.ph.snuggletex.SnuggleSession;
import uk.ac.ed.ph.snuggletex.XMLStringOutputOptions;
import uk.ac.ed.ph.snuggletex.upconversion.UpConvertingPostProcessor;
import uk.ac.ed.ph.snuggletex.upconversion.internal.UpConversionPackageDefinitions;
import uk.ac.ed.ph.snuggletex.upconversion.IllegalUpconversionOptionException;
import uk.ac.ed.ph.snuggletex.upconversion.UpConversionOptionDefinitions;
import uk.ac.ed.ph.snuggletex.upconversion.UpConversionOptions;

import java.io.IOException;

public final class LatextoMathml {
    
    public static void main(String[] args) throws IOException, IllegalUpconversionOptionException {

        //String input = "\\setUpConversionOption{doContentMathML}{true} \\assumeSymbol{f}{function} $f(x)+\\{1,2\\}$";
	String input = args[0];

        /* Set up SnuggleEngine, remembering to register package providing up-conversion support */
        SnuggleEngine engine = new SnuggleEngine();
        engine.addPackage(UpConversionPackageDefinitions.getPackage());
        
        /* Create session in usual way */
        SnuggleSession session = engine.createSession();
        
        /* Parse input. I won't bother checking it here */
        session.parseInput(new SnuggleInput(input));


        /* Create suitable default options */
        UpConversionOptions defaultOptions = new UpConversionOptions();
        defaultOptions.setSpecifiedOption(UpConversionOptionDefinitions.DO_CONTENT_MATHML_NAME, "true");
        defaultOptions.setSpecifiedOption(UpConversionOptionDefinitions.DO_MAXIMA_NAME, "true");
        defaultOptions.setSpecifiedOption(UpConversionOptionDefinitions.ADD_OPTIONS_ANNOTATION_NAME, "true");


        /* Create an UpConvertingPostProcesor that hooks into the DOM generation
         * process to do all of the work. We'll use its (sensible) default behaviour
         * here; options can be passed to this constructor to tweak things.
         */
        UpConvertingPostProcessor upConverter = new UpConvertingPostProcessor();
        
        /* We're going to create a simple XML String output, which we configure
         * as follow. Note how we hook the up-conversion into this options Object.
         */
        XMLStringOutputOptions xmlStringOutputOptions = new XMLStringOutputOptions();
        xmlStringOutputOptions.addDOMPostProcessors(upConverter);
        xmlStringOutputOptions.setIndenting(true);
        xmlStringOutputOptions.setUsingNamedEntities(true);
        
        /* Build up the resulting XML */
        String result = session.buildXMLString(xmlStringOutputOptions);
        System.out.println(result);
    }
}
