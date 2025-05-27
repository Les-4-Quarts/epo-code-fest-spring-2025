export type FullPatent = {
    number: string;
    en_title: string;
    fr_title: string;
    de_title: string;
    en_abstract: string;
    fr_abstract: string;
    de_abstract: string;
    country: string;
    publication_date: string; // YYYYMMDD format
    applicants: Array<{
        name: string;
        patent_number: string;
    }>;
    is_analyzed: boolean;
    description: Array<{
        description_number: number;
        patent_number: string;
        description_text: string;
        sdg?: string | null; // Optional SDG field
    }>;
    claims: Array<{
        claim_number: number;
        patent_number: string;
        claim_text: string;
        sdg?: string | null; // Optional SDG field
    }>;
    sdg_summary?: Array<{
        patent_number: string;
        sdg: string; // e.g., "SDG 1: No Poverty"
        sdg_reason?: string; // Optional reason for SDG relevance
        sdg_details?: string; // Optional detailed explanation
    }>;
}