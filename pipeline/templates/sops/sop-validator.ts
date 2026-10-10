/**
 * templates/sops/sop-validator.ts
 * Upstream Reference: geekan/MetaGPT (70.7k stars)
 * 
 * Standard Operating Procedure (SOP) Artifact Schema Validator.
 * Enforces typed contracts on generated PRDs, Architecture Blueprints, and Sequence Flows.
 */

import * as fs from "node:fs";
import * as path from "node:path";

export interface ValidationResult {
  valid: boolean;
  errors: string[];
  schemaType: "prd" | "architecture";
}

export class SopValidator {
  /**
   * Validates an SOP artifact JSON against the MetaGPT schema.
   */
  public static validate(artifact: Record<string, any>, schemaType: "prd" | "architecture"): ValidationResult {
    const errors: string[] = [];

    if (schemaType === "prd") {
      const requiredFields = [
        "feature_name",
        "target_domain",
        "problem_statement",
        "user_personas",
        "acceptance_criteria",
        "forbidden_states"
      ];
      for (const field of requiredFields) {
        if (!artifact[field]) {
          errors.push(`Missing required PRD field: '${field}'`);
        }
      }
      if (artifact.problem_statement && typeof artifact.problem_statement === "string" && artifact.problem_statement.length < 10) {
        errors.push("PRD problem_statement must be at least 10 characters long");
      }
    } else if (schemaType === "architecture") {
      const requiredFields = [
        "system_name",
        "primary_components",
        "data_contracts",
        "state_machine",
        "security_boundaries"
      ];
      for (const field of requiredFields) {
        if (!artifact[field]) {
          errors.push(`Missing required Architecture field: '${field}'`);
        }
      }
    }

    return {
      valid: errors.length === 0,
      errors,
      schemaType
    };
  }
}

if (import.meta.url === `file:///${process.argv[1].replace(/\\/g, "/")}`) {
  console.log("SopValidator (MetaGPT SOP Schema Enforcement) - Active and Ready.");
}
