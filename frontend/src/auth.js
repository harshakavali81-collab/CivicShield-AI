// OIDC Authorization Code + PKCE integration for an operator-provisioned public client.
// No user accounts, tokens, credentials, or IDP secrets are included in the repository.
import { UserManager } from 'oidc-client-ts';

const authority = import.meta.env.VITE_OIDC_AUTHORITY;
const clientId = import.meta.env.VITE_OIDC_CLIENT_ID;
export const oidcConfigured = import.meta.env.VITE_AUTH_MODE === 'oidc' && !!authority && !!clientId;

export const authManager = oidcConfigured
  ? new UserManager({
    authority,
    client_id: clientId,
    redirect_uri: window.location.origin + window.location.pathname,
    response_type: 'code',
    scope: import.meta.env.VITE_OIDC_SCOPE || 'openid profile',
    automaticSilentRenew: false,
    loadUserInfo: false,
    monitorSession: false,
  })
  : null;

export async function readOidcUser() {
  if (!authManager) return null;
  const query = new URLSearchParams(window.location.search);
  if (query.has('code') && query.has('state')) {
    const user = await authManager.signinRedirectCallback();
    window.history.replaceState({}, document.title, window.location.pathname);
    return user;
  }
  return authManager.getUser();
}

export async function loginWithOidc() {
  if (!authManager) throw new Error('Browser OIDC is not configured');
  await authManager.signinRedirect();
}
export async function logoutLocally() {
  if (authManager) await authManager.removeUser();
}
