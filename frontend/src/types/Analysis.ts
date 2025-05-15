export type Analysis = {
    classified_description: {
        sdg: string;
        text: string;
    }[];
    sdg_summary: {
        patent_number: string;
        sdg: string;
        sdg_description: string;
    }[];
}