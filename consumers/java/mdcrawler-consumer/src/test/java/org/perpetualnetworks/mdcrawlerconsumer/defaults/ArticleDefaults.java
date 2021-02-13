package org.perpetualnetworks.mdcrawlerconsumer.defaults;

import com.google.common.collect.ImmutableSet;
import org.perpetualnetworks.mdcrawlerconsumer.models.Article;
import org.perpetualnetworks.mdcrawlerconsumer.models.FileArticle;

import java.util.Arrays;
import java.util.Collections;
import java.util.Set;

public class ArticleDefaults {
    static String TITLE = "test title";
    static String SOURCE_URL = "https://test.com/test";
    static Set<String> KEYWORDS = ImmutableSet.copyOf(Arrays.asList("word 1", "word 2", "word3", "WORD"));
    static String DOI = "10.12053/2016-026x-1x-2x9";
    static String DESC = "test description";
    static String PARSE_DATE = "1970-01-01T00:00:00";
    static String UPLOAD_DATE = "1970-01-01T00:00:00";
    static String CREATED_DATE = "1970-01-01T00:00:00";
    static String MODIFIED_DATE = "1970-01-01T00:00:00";
    static Set<FileArticle> FILES = Collections.singleton(
            FileArticle.builder()
                    .downloadUrl("https://filedownload/test")
                    .fileName("test file")
                    .digitalObjectId("10.12.000/2016-027x-1x-2x9")
                    .fileDescription("bob")
                    .referingUrl("https://alice.wl")
                    .keywords(Collections.singleton("cat"))
                    .build());
    static String REFERING_URL = "http://test.refering.url.com";
    static Boolean ENRICHED = false;
    static Boolean PUBLISHED = true;
    static Boolean PARSED = true;

    public static Article.ArticleBuilder anArticle() {
        return Article.builder()
                .title(TITLE)
                .sourceUrl(SOURCE_URL)
                .keywords(KEYWORDS)
                .digitalObjectId(DOI)
                .description(DESC)
                .parseDate(PARSE_DATE)
                .uploadDate(UPLOAD_DATE)
                .createdDate(CREATED_DATE)
                .modifiedDate(MODIFIED_DATE)
                .files(FILES)
                //.authors()
                .referingUrl(REFERING_URL)
                .enriched(ENRICHED)
                .published(PUBLISHED)
                .parsed(PARSED)
                .additionalData(Article.AdditionalData.builder().build());
    }

}
