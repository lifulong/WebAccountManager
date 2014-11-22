#!/usr/bin/env	python
# -*- coding:utf-8 -*-

"""
This file implement the tcp server for account-manager.

Multi Thread.
"""

__version__ = "0.1"

DEFAULT_ERROR_MESSAGE = """
Error Code:%(code)d.
Message:%(message)s.
Code Explain:%(explain)s.
"""

DEFAULT_ERROR_CONTENT_TYPE = "text/html"

import sys
import time
import socket # For gethostbyaddr()
import json
from warnings import filterwarnings, catch_warnings
with catch_warnings():
    if sys.py3kwarning:
        filterwarnings("ignore", ".*mimetools has been removed",
                        DeprecationWarning)
    import mimetools

from config import *
from socket_svr import *


class AMRequestHandler(StreamRequestHandler):

	"""account-manager(AM) svr request handler base class.
	"""

	# The Python system version, truncated to its first component.
	sys_version = "Python/" + sys.version.split()[0]

	# The server software version.  You may want to override this.
	# The format is multiple whitespace-separated strings,
	# where each string is of the form name[/version].
	server_version = "BaseAM/" + __version__

	# The default request version.  This only affects responses up until
	# the point where the request line is parsed, so it mainly decides what
	# the client gets back when sending a malformed request line.
	# Most web servers default to AM 0.1, i.e. don't send a status line.
	default_request_version = "AM/0.1"

	def parse_request(self):
		"""Parse a request (internal).

		The request should be stored in self.raw_requestline; the results
		are in self.command, self.path, self.request_version and
		self.headers.

		Return True for success, False for failure; on failure, an
		error is sent back.

		"""
		self.command = None  # set in case of error on the first line
		self.request_version = version = self.default_request_version
		self.close_connection = 1
		requestline = self.raw_requestline
		requestline = requestline.rstrip('\r\n')
		self.requestline = requestline
		words = requestline.split()
		if len(words) == 3:
			command, path, version = words
			if version[:5] != 'AM/':
				self.send_error(400, "Bad request version (%r)" % version)
				return False
			try:
				base_version_number = version.split('/', 1)[1]
				version_number = base_version_number.split(".")
				# RFC 2145 section 3.1 says there can be only one "." and
				#   - major and minor numbers MUST be treated as
				#	  separate integers;
				#   - Leading zeros MUST be ignored by recipients.
				if len(version_number) != 2:
					raise ValueError
				version_number = int(version_number[0]), int(version_number[1])
			except (ValueError, IndexError):
				self.send_error(400, "Bad request version (%r)" % version)
				return False
			if version_number >= (1, 1) and self.protocol_version >= "AM/1.1":
				self.close_connection = 0
			if version_number >= (2, 0):
				self.send_error(505,
						  "Invalid AM Version (%s)" % base_version_number)
				return False
		elif len(words) == 2:
			command, path = words
			self.close_connection = 1
			if command != 'GET':
				self.send_error(400,
								"Bad AM/0.9 request type (%r)" % command)
				return False
		elif not words:
			return False
		else:
			self.send_error(400, "Bad request syntax (%r)" % requestline)
			return False
		self.command, self.path, self.request_version = command, path, version

		# Examine the headers and look for a Connection directive
		self.headers = self.MessageClass(self.rfile, 0)

		conntype = self.headers.get('Connection', "")
		if conntype.lower() == 'close':
			self.close_connection = 1
		elif (conntype.lower() == 'keep-alive' and
			  self.protocol_version >= "AM/1.1"):
			self.close_connection = 0
		return True

	def handle_one_request(self):
		"""Handle a single AM request.

		You normally don't need to override this method; see the class
		__doc__ string for information on how to handle specific AM
		commands such as GET and POST.

		"""
		try:
			self.raw_requestline = self.rfile.readline(65537)
			if len(self.raw_requestline) > 65536:
				self.requestline = ''
				self.request_version = ''
				self.command = ''
				self.send_error(414)
				return
			if not self.raw_requestline:
				self.close_connection = 1
				return
			if not self.parse_request():
				# An error code has been sent, just exit
				return
			mname = 'do_' + self.command
			if not hasattr(self, mname):
				self.send_error(501, "Unsupported method (%r)" % self.command)
				return
			method = getattr(self, mname)
			method()
			self.wfile.flush() #actually send the response if not already done.
		except socket.timeout, e:
			#a read or a write timed out.  Discard this connection
			self.log_error("Request timed out: %r", e)
			self.close_connection = 1
			return

	def handle(self):
		"""Handle multiple requests if necessary."""
		self.close_connection = 1

		self.handle_one_request()
		while not self.close_connection:
			self.handle_one_request()

	def send_error(self, code, message=None):
		"""Send and log an error reply.

		Arguments are the error code, and a detailed message.
		The detailed message defaults to the short entry matching the
		response code.

		This sends an error response (so it must be called before any
		output has been generated), logs the error, and finally sends
		a piece of HTML explaining the error to the user.

		"""

		try:
			short, long = self.responses[code]
		except KeyError:
			short, long = '???', '???'
		if message is None:
			message = short
		explain = long
		self.log_error("code %d, message %s", code, message)
		# using _quote_html to prevent Cross Site Scripting attacks (see bug #1100201)
		content = (self.error_message_format %
				   {'code': code, 'message': _quote_html(message), 'explain': explain})
		self.send_response(code, message)
		self.send_header("Content-Type", self.error_content_type)
		self.send_header('Connection', 'close')
		self.end_headers()
		if self.command != 'HEAD' and code >= 200 and code not in (204, 304):
			self.wfile.write(content)

	error_message_format = DEFAULT_ERROR_MESSAGE
	error_content_type = DEFAULT_ERROR_CONTENT_TYPE

	def send_response(self, code, message=None):
		"""Send the response header and log the response code.

		Also send two standard headers with the server software
		version and the current date.

		"""
		self.log_request(code)
		if message is None:
			if code in self.responses:
				message = self.responses[code][0]
			else:
				message = ''
		if self.request_version != 'AM/0.9':
			self.wfile.write("%s %d %s\r\n" %
							 (self.protocol_version, code, message))
			# print (self.protocol_version, code, message)
		self.send_header('Server', self.version_string())
		self.send_header('Date', self.date_time_string())

	def send_header(self, keyword, value):
		"""Send a MIME header."""
		if self.request_version != 'AM/0.9':
			self.wfile.write("%s: %s\r\n" % (keyword, value))

		if keyword.lower() == 'connection':
			if value.lower() == 'close':
				self.close_connection = 1
			elif value.lower() == 'keep-alive':
				self.close_connection = 0

	def end_headers(self):
		"""Send the blank line ending the MIME headers."""
		if self.request_version != 'AM/0.9':
			self.wfile.write("\r\n")

	def log_request(self, code='-', size='-'):
		"""Log an accepted request.

		This is called by send_response().

		"""

		self.log_message('"%s" %s %s',
						 self.requestline, str(code), str(size))

	def log_error(self, format, *args):
		"""Log an error.

		This is called when a request cannot be fulfilled.  By
		default it passes the message on to log_message().

		Arguments are the same as for log_message().

		XXX This should go to the separate error log.

		"""

		self.log_message(format, *args)

	def log_message(self, format, *args):
		"""Log an arbitrary message.

		This is used by all other logging functions.  Override
		it if you have specific logging wishes.

		The first argument, FORMAT, is a format string for the
		message to be logged.  If the format string contains
		any % escapes requiring parameters, they should be
		specified as subsequent arguments (it's just like
		printf!).

		The client ip address and current date/time are prefixed to every
		message.

		"""

		sys.stderr.write("%s - - [%s] %s\n" %
						 (self.client_address[0],
						  self.log_date_time_string(),
						  format%args))

	def version_string(self):
		"""Return the server software version string."""
		return self.server_version + ' ' + self.sys_version

	def date_time_string(self, timestamp=None):
		"""Return the current date and time formatted for a message header."""
		if timestamp is None:
			timestamp = time.time()
		year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
		s = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
				self.weekdayname[wd],
				day, self.monthname[month], year,
				hh, mm, ss)
		return s

	def log_date_time_string(self):
		"""Return the current time formatted for logging."""
		now = time.time()
		year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
		s = "%02d/%3s/%04d %02d:%02d:%02d" % (
				day, self.monthname[month], year, hh, mm, ss)
		return s

	weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

	monthname = [None,
				 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
				 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

	def address_string(self):
		"""Return the client address formatted for logging.

		This version looks up the full hostname using gethostbyaddr(),
		and tries to find a name that contains at least one dot.

		"""

		host, port = self.client_address[:2]
		return socket.getfqdn(host)

	# Essentially static class variables

	# The version of the AM protocol we support.
	# Set this to AM/1.1 to enable automatic keepalive
	protocol_version = "AM/1.0"

	# The Message-like class used to parse headers
	MessageClass = mimetools.Message

	# Table mapping response codes to messages; entries have the
	# form {code: (shortmessage, longmessage)}.
	# See RFC 2616.
	responses = {
		100: ('Continue', 'Request received, please continue'),
		101: ('Switching Protocols',
			  'Switching to new protocol; obey Upgrade header'),

		200: ('OK', 'Request fulfilled, document follows'),
		201: ('Created', 'Document created, URL follows'),
		202: ('Accepted',
			  'Request accepted, processing continues off-line'),
		203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
		204: ('No Content', 'Request fulfilled, nothing follows'),
		205: ('Reset Content', 'Clear input form for further input.'),
		206: ('Partial Content', 'Partial content follows.'),

		300: ('Multiple Choices',
			  'Object has several resources -- see URI list'),
		301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
		302: ('Found', 'Object moved temporarily -- see URI list'),
		303: ('See Other', 'Object moved -- see Method and URL list'),
		304: ('Not Modified',
			  'Document has not changed since given time'),
		305: ('Use Proxy',
			  'You must use proxy specified in Location to access this '
			  'resource.'),
		307: ('Temporary Redirect',
			  'Object moved temporarily -- see URI list'),

		400: ('Bad Request',
			  'Bad request syntax or unsupported method'),
		401: ('Unauthorized',
			  'No permission -- see authorization schemes'),
		402: ('Payment Required',
			  'No payment -- see charging schemes'),
		403: ('Forbidden',
			  'Request forbidden -- authorization will not help'),
		404: ('Not Found', 'Nothing matches the given URI'),
		405: ('Method Not Allowed',
			  'Specified method is invalid for this resource.'),
		406: ('Not Acceptable', 'URI not available in preferred format.'),
		407: ('Proxy Authentication Required', 'You must authenticate with '
			  'this proxy before proceeding.'),
		408: ('Request Timeout', 'Request timed out; try again later.'),
		409: ('Conflict', 'Request conflict.'),
		410: ('Gone',
			  'URI no longer exists and has been permanently removed.'),
		411: ('Length Required', 'Client must specify Content-Length.'),
		412: ('Precondition Failed', 'Precondition in headers is false.'),
		413: ('Request Entity Too Large', 'Entity is too large.'),
		414: ('Request-URI Too Long', 'URI is too long.'),
		415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
		416: ('Requested Range Not Satisfiable',
			  'Cannot satisfy request range.'),
		417: ('Expectation Failed',
			  'Expect condition could not be satisfied.'),

		500: ('Internal Server Error', 'Server got itself in trouble'),
		501: ('Not Implemented',
			  'Server does not support this operation'),
		502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
		503: ('Service Unavailable',
			  'The server cannot process the request due to a high load'),
		504: ('Gateway Timeout',
			  'The gateway server did not receive a timely response'),
		505: ('AM Version Not Supported', 'Cannot fulfill request.'),
		}


	def send_head(self):
        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

	def parse_real_request(self):
		""" Parse json request string (key, value) dict (Internal).

			return dict.
		"""

		pass

	def append_result(self, key, value):
		"""	Append key&value to result dict.
		"""

		self.result[key] = value;


	def make_real_result(self):
		"""	Make obj string to json string.

			return json string.
		"""

		self.json_result = json.dumps(self.result, sort_keys=True, separators=(',',':'))

	def send_result(self):
		""" Send json_result to client.
		"""

		self.wfile.write(self.json_result)

	def do_VERSION(self):
		self.send_head()
		self.append_result("VERSION", AMRequestHandler.server_version)
		self.make_real_result()
		self.send_result()

	def do_REGISTER(self):
		self.send_head()
		self.append_result("ERRNO", "{0}".format(self.errno))
		self.make_real_result()
		self.send_result()

	def do_LOGIN(self):
		pass

	def do_LOGOUT(self):
		pass

	def do_GET(self):
		pass

	def do_POST(self):
		pass

	def do_DEL(self):
		pass

	def do_MOD(self):
		pass




class AccountManagerSvr(ThreadingTCPServer):
	""" TCP Svr of account-manager.
	"""

	allow_reuse_address = 1	# Seems to make sense in testing environment

	"""
	def __init__(self, config_file):

		#super(ThreadingTCPServer, self).__init__(address, AMRequestHandler)
		#ThreadingTCPServer.__init__(address, AMRequestHandler)

		if __debug__ :
			print "Address is %s:%d.", address
	"""

	def server_bind(self):
		"""Override server_bind to store the server name."""
		TCPServer.server_bind(self)
		host, port = self.socket.getsockname()[:2]
		self.server_name = socket.getfqdn(host)
		self.server_port = port



def test(config_file):
	"""Test the account-manager svr.
	"""

	config(config_file)

	address = (config.config_tcp_svr_addr, config.config_tcp_svr_port)

	svr = AccountManagerSvr(address, AMRequestHandler)

	sa = svr.socket.getsockname()

	print "account-manager Tcp Server Serving on ", sa[0], " port ", sa[1], " ..."

	svr.serve_forever()

if __name__ == '__main__':

	test("_config.json")


