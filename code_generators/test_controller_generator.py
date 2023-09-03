import re
from textwrap import dedent

from __init__ import _6_TABS, EMPTY
from directory_handler import create_test_directories
from language_dictionary import LocalizationDict
from utils import camel_to_pascal, pascal_to_camel

from .base_generator import BaseGenerator


class TestGenerator(BaseGenerator):

	def __init__(self, group_name: str, entity_name: str, language_dict: LocalizationDict, fields_input: str, table_name: str, table_schema: str, jdk_version: str, complete_package_path: str):
		super().__init__(group_name, entity_name, language_dict, fields_input, table_name, table_schema, jdk_version, create_test_directories(group_name.replace('.', '-'), group_name))

	def generate(self):
		entity_name_kebab = ''.join(word.lower() if i == 0 else '-' + word.lower() for i, word in enumerate(re.findall('[A-Z][^A-Z]*', self.entity_name)))
		controller_name = f"{camel_to_pascal(self.entity_name)}Controller"
		controller_name_camel = pascal_to_camel(controller_name)
		service_name = f"{self.entity_name}Service"
		entity_name = f"{camel_to_pascal(self.entity_name)}"
		service_field_name = f"{pascal_to_camel(self.entity_name)}Service"
		entity_name_camel = pascal_to_camel(self.entity_name)
		vo_name = f"{camel_to_pascal(self.entity_name)}VO";
		vo_name_camel = f"{entity_name_camel}VO"
		controller_route = f"/{'/'.join(entity_name_kebab.split('-'))}"

		test_controller_code = dedent(f"""\
				package {self.group_name};

				import {self.group_name}.entity.{entity_name};
				import {self.group_name}.services.{service_name};
				import {self.group_name}.vo.{self.entity_name}VO;
				import {self.group_name}.request.{self.entity_name}Request;

				import org.junit.jupiter.api.BeforeEach;
				import org.junit.jupiter.api.Test;
				import org.springframework.boot.test.context.SpringBootTest;
				import org.springframework.data.domain.Page;
				import org.springframework.data.domain.Pageable;
				import org.springframework.data.web.PageableDefault;
				import org.springframework.data.domain.Sort.Direction;
				import org.springframework.data.web.PageableDefault;
				import org.mockito.InjectMocks;
				import org.mockito.Mock;
				import org.mockito.MockitoAnnotations;
				import org.springframework.test.web.servlet.MockMvc;
				import org.springframework.test.web.servlet.setup.MockMvcBuilders;

				import static org.mockito.Mockito.*;
				import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
				import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

				import com.fasterxml.jackson.databind.ObjectMapper;

				@SpringBootTest
				public class {controller_name}Controller {{

						@InjectMocks
						private {controller_name} {controller_name_camel};

						@Autowired
						private {service_name} {service_field_name};

						private MockMvc mockMvc;

						@BeforeEach
						void setUp() {{
								MockitoAnnotations.openMocks(this);
								mockMvc = MockMvcBuilders.standaloneSetup({controller_name_camel}).build();
						}}

						@Test
						void test{camel_to_pascal(self.language_dict.get_text('listWithFilters'))}() throws Exception {{
								{self.entity_name}Request request = new {self.entity_name}Request();
								Pageable pageable = Pageable.unpaged();
								Page<{vo_name}> page = mock(Page.class);

								when({service_field_name}.{self.language_dict.get_text('listVoWithFilters')}(any({self.entity_name}Request.class), any(Pageable.class))).thenReturn(page);

								mockMvc.perform(get("{controller_route}"))
										.andExpect(status().isOk());

								verify({service_field_name}, times(1)).{self.language_dict.get_text('listVoWithFilters')}(any({self.entity_name}Request.class), any(Pageable.class));
						}}

						@Test
						void test{camel_to_pascal(self.language_dict.get_text('findById'))}() throws Exception {{
								{vo_name} c = new {vo_name}();
								when({service_field_name}.{self.language_dict.get_text('findVoById')}(1L)).thenReturn({vo_name_camel});

								mockMvc.perform(get("{controller_route}/1"))
										.andExpect(status().isOk());

								verify({service_field_name}, times(1)).{self.language_dict.get_text('findVoById')}(1L);
						}}

						@Test
						void test{camel_to_pascal(self.language_dict.get_text('saveEntity'))}() throws Exception {{
								Long id = 1L;

								// Perform and Verify
								mockMvc.perform(post("{controller_route}/" + id))
										.andExpect(status().isOk());

								verify({service_field_name}, times(1)).self.language_dict.get_text('saveEntity')(eq(id));
						}}

						@Test
						void test{camel_to_pascal(self.language_dict.get_text('updateEntity'))}() throws Exception {{
								Long id = 1L;

								// Perform and Verify
								mockMvc.perform(put("{controller_route}/" + id))
										.andExpect(status().isOk());

								verify({service_field_name}, times(1)).updateEntity(eq(id));
						}}

						@Test
						void test{camel_to_pascal(self.language_dict.get_text('deleteEntity'))}() throws Exception {{
								Long id = 1L;

								// Perform and Verify
								mockMvc.perform(delete("{controller_route}/" + id))
										.andExpect(status().isAccepted());

								verify({service_field_name}, times(1)).logicalDelete(eq(id));
						}}

				}}
		""")
		self.write_to_java_file(f"{self.complete_package_path}", f"{controller_name}Test", test_controller_code)
