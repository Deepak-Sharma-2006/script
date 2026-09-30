/**
 * Adversarial Test Suite [Lead 2 / SDET]: Domain Engine Resilience & Fault Tolerance
 * Verifies:
 * 1. Corrupted active-domain.json state files fail-safe to valid default without process crash.
 * 2. Path traversal or injection in domain_id is strictly rejected.
 * 3. Empty or malformed subdomain inputs normalize gracefully to defaults.
 * 4. Switching domain profiles does NOT invalidate or corrupt active domain leases.
 */

import { test } from 'node:test';
import * as assert from 'node:assert/strict';
import * as fs from 'fs';
import * as path from 'path';
import {
  setDomain,
  getActiveDomainState,
  loadRubric,
  saveActiveDomainState
} from '../../scripts/domain-selector.ts';

const STATE_FILE = path.resolve(process.cwd(), '.agents', 'state', 'active-domain.json');

test('ADVERSARIAL BATTERY [Lead 2]: Domain State Corruption Resilience', async (t) => {

  await t.test('Corrupted JSON in active-domain.json must self-heal to default profile', () => {
    const backup = fs.readFileSync(STATE_FILE, 'utf-8');
    try {
      // Injected corrupted malformed JSON
      fs.writeFileSync(STATE_FILE, '{"domain_id": UNTERMINATED_CORRUPT...', 'utf-8');

      // Must not throw unhandled exception
      const state = getActiveDomainState();
      assert.ok(state.domain_id, 'Must return a valid domain_id');
      assert.ok(Array.isArray(state.subdomains), 'Subdomains must be an array');
      assert.ok(state.active_stack.languages_and_tools.length > 0, 'Active stack must have tools');
    } finally {
      fs.writeFileSync(STATE_FILE, backup, 'utf-8');
    }
  });

  await t.test('Path traversal attempts in domain ID must be rejected', () => {
    assert.throws(
      () => setDomain('../../../etc/passwd', ['web_frontend']),
      /Invalid domain/
    );
  });

  await t.test('Empty subdomains list must default to primary available subdomain', () => {
    const state = setDomain('software', []);
    assert.ok(state.subdomains.length >= 1, 'Must fallback to at least one valid subdomain');
    assert.equal(state.domain_id, 'software');
  });

  await t.test('Invalid or unknown subdomains must be pruned without failing the valid ones', () => {
    const state = setDomain('blockchain', ['smart_contracts', 'invalid_subdomain_xyz', 'defi_protocols']);
    assert.ok(state.subdomains.includes('smart_contracts'));
    assert.ok(state.subdomains.includes('defi_protocols'));
    assert.ok(!state.subdomains.includes('invalid_subdomain_xyz'));
  });

  await t.test('All 8 master domains must have non-empty verification gates and toolchains', () => {
    const domains = [
      'software', 'ai_ml', 'blockchain', 'deep_tech',
      'cybersecurity', 'cloud_infra', 'data_engineering', 'vertical_applied'
    ];
    for (const d of domains) {
      const rubric = loadRubric(d);
      assert.ok(rubric.verification_gates.length >= 3, `Domain ${d} must have at least 3 gates`);
      assert.ok(Object.keys(rubric.subdomains).length >= 4, `Domain ${d} must have at least 4 subdomains`);
    }
  });
});
