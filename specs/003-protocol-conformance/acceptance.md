# Acceptance evidence — 003

Evidence IDs map to protocol tests: AC-201 test_direct_text_and_correct_route/test_group_text_and_route; AC-202 test_direct_and_group_receipt_correlation_inputs; AC-203 test_typing_both_scopes; AC-204 test_media_is_metadata_not_download/test_group_status_contains_no_untrusted_admin_authority; AC-205 test_iq_results_are_not_authority; AC-206 negative XML, JID, ID, size, group and receipt tests. All use synthetic fixtures and no network.

CI evidence: [Actions run 36571522205](https://github.com/canstralian/kik-bot-api-unofficial/actions/runs/36571522205) passed 35 offline tests on Python 3.10/3.11 plus strict third-party audit, source/wheel build, installed-wheel import and Docker image build at f8559f2. Revalidate any later PR-head changes before merge. No Kik service interoperability or exactly-once message delivery claim is in scope.
