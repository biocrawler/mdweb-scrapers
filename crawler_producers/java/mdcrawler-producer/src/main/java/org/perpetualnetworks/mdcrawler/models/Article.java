package org.perpetualnetworks.mdcrawler.models;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Builder;
import lombok.Data;

import java.util.List;
import java.util.Set;

@Data
@Builder(toBuilder = true)
public class Article {
    @JsonProperty
    private String title;
    @JsonProperty("source_url")
    private String sourceUrl;
    @JsonProperty
    private Set<String> keywords;
    @JsonProperty("digital_object_id")
    private String digitalObjectId;
    @JsonProperty
    private String description;
    @JsonProperty("parse_date")
    private String parseDate;
    @JsonProperty("upload_date")
    private String uploadDate;
    @JsonProperty
    private Set<FileArticle> files;
    @JsonProperty
    private Set<Author> authors;
    @JsonProperty("refering_url")
    private String referingUrl;  //was parent request url
    @JsonProperty
    private Boolean enriched;
    @JsonProperty
    private Boolean published;
    @JsonProperty("additional_data")
    private AdditionalData additionalData;

    @Data
    @Builder(toBuilder = true)
    public static class AdditionalData {
        @JsonProperty("figshare_type")
        private String figshareType;
        @JsonProperty("lab_details")
        private List<String> labDetails;
    }

}
